import argparse
import requests
from typing import Dict, List
from datetime import datetime, timedelta
from pyntcli import __version__ as cli_version
from pyntcli.analytics import send as analytics
from pyntcli.transport import pynt_requests
from pyntcli.ui import ui_thread
from pyntcli.ui import prompt
from pyntcli.store import CredStore, StateStore
import pyntcli.log.log as log

from requests.exceptions import SSLError, HTTPError

from . import command, listen, postman, root, sub_command, id_command, newman, har, burp, template

logger = log.get_logger()

avail_sub_commands = [
    postman.PostmanSubCommand("postman"),
    id_command.PyntShowIdCommand("pynt-id"),
    newman.NewmanSubCommand("newman"),
    har.HarSubCommand("har"),
    command.CommandSubCommand("command"),
    listen.ListenSubCommand("listen"),
    burp.BurpCommand("burp"),
    template.TemplateSubCommand("template")
]

commands_without_app_id = ["postman", "pynt-id"]


class PyntCommandException(Exception):
    pass


class UserAbortedException(Exception):
    pass


class BadArgumentsException(PyntCommandException):
    pass


class NoSuchCommandException(PyntCommandException):
    pass


VERSION_CHECK_URL = "https://d1efigcr4c19qn.cloudfront.net/cli/version"


def check_is_latest_version(current_version):
    try:
        res = pynt_requests.get(VERSION_CHECK_URL)
        res.raise_for_status()

        latest_versions = res.text.replace("\n", "")

        if current_version != latest_versions:
            ui_thread.print(ui_thread.PrinterText("""Pynt CLI new version is available, upgrade now with:
python3 -m pip install --upgrade pyntcli""", ui_thread.PrinterText.WARNING))
    except SSLError:
        ui_thread.print(ui_thread.PrinterText(
            """Error: Unable to check if Pynt CLI version is up-to-date due to VPN/proxy. Run Pynt with --insecure to fix.""", ui_thread.PrinterText.WARNING))
    except HTTPError:
        ui_thread.print(
            """Unable to check if Pynt CLI version is up-to-date""")
    except Exception as e:
        ui_thread.print(ui_thread.PrinterText(
            """We could not check for updates.""", ui_thread.PrinterText.WARNING))
        pass


class PyntCommand:
    def __init__(self) -> None:
        self.base: root.BaseCommand = root.BaseCommand()
        self.sub_commands: Dict[str, sub_command.PyntSubCommand] = {
            sc.get_name(): sc for sc in avail_sub_commands}
        self._start_command()

    def _start_command(self):
        self.base.cmd()
        for sc in self.sub_commands.values():
            self.base.add_base_arguments(sc.add_cmd(self.base.get_subparser()))

    def parse_args(self, args_from_cmd: List[str]):
        return self.base.cmd().parse_args(args_from_cmd)

    def run_cmd(self, args: argparse.Namespace):
        if not "command" in args:
            raise BadArgumentsException()

        command = getattr(args, "command")
        if not command in self.sub_commands:
            raise NoSuchCommandException()
        check_is_latest_version(cli_version)
        analytics.emit(analytics.CLI_START)
        if "host_ca" in args and args.host_ca:
            pynt_requests.add_host_ca(args.host_ca)

        if "insecure" in args and args.insecure:
            pynt_requests.disable_tls_termination()

        self.base.run_cmd(args)

        # Some args are recommended/required for business-plan users.
        # These can be verified only after running 'self.base.run_cmd()' where the login occurs
        is_business_plan_user = self._is_business_plan_user()
        try:
            self._post_login_args_validation(
                args, command, is_business_plan_user)
        except UserAbortedException as e:
            ui_thread.print("Aborting...")
            return

        self.sub_commands[command].run_cmd(args)

    def _is_business_plan_user(self):
        """ 
        A workaround for checking whether it's a free tier user or not
        by try accessing api.pynt.io/v1/config (it's a free tier if the user can't access it)

        Returns:
            bool: True if it's a business-plan user
        """
        saas_url = "https://api.pynt.io/v1/config"
        headers = {}
        with CredStore() as store:
            access_keys = store.get_access_token()
            token_type = store.get_token_type()
            headers["Authorization"] = f"{token_type} {access_keys}"
        try:
            response = requests.get(saas_url, headers=headers, timeout=10)

            if response.status_code == requests.codes.ok:
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            # Catch all other request exceptions
            logger.debug(f"An error occurred when accessing '{saas_url}': {e}")
            return False

    def _post_login_args_validation(self, args: argparse.Namespace, command: str, is_business_plan_user: bool):
        if getattr(args, "application_name"):
            if getattr(args, "yes") or self._is_auto_create_app_confirmed(args.application_name):
                return
            else:
                raise UserAbortedException()

        # Confirm not using application-id flag if applicable
        if getattr(args, "application_id") or command in commands_without_app_id:
            return

        # For a business user, it's recommended to always provide the application-id.
        if is_business_plan_user:
            if getattr(args, "yes") or self._is_missing_app_id_confirmed():
                return
            else:
                raise UserAbortedException()

    def is_confirmed(self, prompt_history_key: str, confirmation_message: str, default_confirmation: str) -> bool:
        """
               Ask for the user's confirmation to continue if he/she wasn't asked in the last week.

               Returns:
                   bool: True if the user confirms or he/she has confirmed once in the last week. Otherwise, returns False
               """
        with StateStore() as state_store:
            current_time = datetime.now()
            prompts_history = state_store.get_prompts_history()
            last_confirmed = prompts_history.get(
                prompt_history_key, {}).get("last_confirmation", "")
            if last_confirmed:
                # Calculate the time delta
                parsed_datetime = datetime.strptime(
                    last_confirmed, "%Y-%m-%d %H:%M:%S")
                difference = current_time - parsed_datetime
                if difference < timedelta(days=7):
                    return True

            if prompt.confirmation_prompt_with_timeout(confirmation_message, default=default_confirmation, timeout=15):
                prompts_history["missing_app_id"] = {"last_confirmation": current_time.strftime("%Y-%m-%d %H:%M:%S")}
                state_store.put_prompts_history(
                    prompts_history)
                return True

        return False

    def _is_missing_app_id_confirmed(self) -> bool:
        return self.is_confirmed("missing_app_id", "Application ID is missing. Use the '--application-id' flag to provide it.\n" +
                                                       "Without an Application ID, the scan will not be associated with your application.\n" +
                                                       "The Application ID can be fetched from https://app.pynt.io/dashboard/applications.\n" +
                                                       "Do you want to continue without associating the scan?", "yes")


    def _is_auto_create_app_confirmed(self, application_name: str) -> bool:
        return self.is_confirmed("auto_create_application", f"Application {application_name} will be created automatically if it does not exist.\n" +
                                                       f"Do you want to continue without the application name {application_name}?", "yes")
