import json
import MT5Manager

from typing import List
from nostro_mt5_manager_v1.dealer_sink import DealerSink
from nostro_mt5_manager_v1.manager_helper import ManagerHelper


class Manager:
    def __init__(self, mt5_server: str, mt5_login: int, mt5_password: str):
        self.__manager = MT5Manager.ManagerAPI()

        self.mt5_server = mt5_server
        self.mt5_login = mt5_login
        self.mt5_password = mt5_password

        self.connected = False

    def connect(self):
        try:
            assert isinstance(self.mt5_server, str), "mt5_server must be a string"
            assert isinstance(self.mt5_login, int), "mt5_server must be an integer"
            assert isinstance(self.mt5_password, str), "mt5_server must be a string"

            response = self.__manager.Connect(
                self.mt5_server,
                int(self.mt5_login),
                self.mt5_password,
                MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_FULL,
                30000,
            )

            if(response == True):
                self.connected = True
                return {"status": "connected", "error": None}
            else:
                return {"status": "not connected", "error": None}      
                  
        except Exception as e:
            return {"status": "not connected", "error": str(e)}

    def disconnect(self):
        try:
            self.__manager.Disconnect()
            self.connected = False
        except Exception as e:
            print(f"Error disconnecting: {str(e)}")

    def get_user_by_id(self, login: int) -> MT5Manager.MTUser:
        try:
            assert self.connected, "mt5_server must be connected"

            user = MT5Manager.MTUser(self.__manager)

            user: MT5Manager.MTUser = self.__manager.UserGet(login)

            if not user:
                raise Exception("error fetching user")
            else:
                return user
        except Exception as e:
            print(f"Error getting user by ID: {str(e)}")
            return None

    def create_mt5_account(
        self,
        name: str,
        email: str,
        group: str,
        initial_balance: float,
        initial_target: float,
        leverage: int,
    ) -> tuple:
        try:
            assert self.connected, "mt5_server must be connected"

            temp_main_password = ManagerHelper.generate_temp_password(15)
            temp_investor_password = ManagerHelper.generate_temp_password(15)

            user = MT5Manager.MTUser(self.__manager)

            user.Name = name
            user.EMail = email
            user.Color = 3329330
            user.Group = group
            user.Company = str(initial_balance)
            user.LeadCampaign = str(initial_target)
            user.Rights = (
                MT5Manager.MTUser.EnUsersRights.USER_RIGHT_DEFAULT
                | MT5Manager.MTUser.EnUsersRights.USER_RIGHT_TRADE_DISABLED
            )
            user.Leverage = leverage

            user_created: MT5Manager.MTUser = self.__manager.UserAdd(
                user, temp_main_password, temp_investor_password
            )

            if not user_created:
                raise Exception("Couldn't create account")

            login = user.Login

            balance_added = self.__manager.DealerBalance(
                login, initial_balance, 5, "Initial Balance"
            )

            if not balance_added:
                raise Exception("Couldn't add balance to user account")

            user.Rights = (
                MT5Manager.MTUser.EnUsersRights.USER_RIGHT_EXPERT
                | MT5Manager.MTUser.EnUsersRights.USER_RIGHT_ENABLED
            )

            user_updated = self.__manager.UserUpdate(user)

            if not user_updated:
                raise Exception("Couldn't update user")

            return (login, temp_main_password, temp_investor_password)
        except Exception as e:
            print(f"Error creating MT5 account: {str(e)}")
            return None

    def get_trade_accounts_in_group(self, group: str) -> List[int]:
        try:
            assert self.connected, "mt5_server must be connected"

            users = self.__manager.UserGetByGroup(group)

            return [user.Login for user in users]
        except Exception as e:
            print(f"Error getting trade accounts in group: {str(e)}")
            return []

    def reset_password(self, login: int):
        try:
            assert self.connected, "mt5_server must be connected"

            temp_main_password = ManagerHelper.generate_temp_password(15)

            password_main_changed = self.__manager.UserPasswordChange(
                MT5Manager.MTUser.EnUsersPasswords.USER_PASS_MAIN,
                login,
                temp_main_password,
            )

            if not password_main_changed:
                raise Exception("there was an error resetting main password")

            temp_investor_password = ManagerHelper.generate_temp_password(15)

            password_investor_changed = self.__manager.UserPasswordChange(
                MT5Manager.MTUser.EnUsersPasswords.USER_PASS_INVESTOR,
                login,
                temp_investor_password,
            )

            if not password_investor_changed:
                raise Exception("there was an error resetting investor password")

            return (temp_main_password, temp_investor_password)
        except Exception as e:
            print(f"Error resetting password: {str(e)}")
            return None

    def change_user_group(self, login: int, group: str) -> bool:
        try:
            assert self.connected, "mt5_server must be connected"

            trade_user: MT5Manager.MTUser = self.__manager.UserGet(login)

            if not trade_user:
                return {"message": "Trade user not found"}

            trade_user.Group = group

            group_changed = self.__manager.UserUpdate(trade_user)

            if group_changed:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error changing user group: {str(e)}")
            return False

    def delete_pending_orders(self, login: int) -> bool:
        try:
            assert self.connected, "mt5_server must be connected"

            open_orders = self.__manager.OrderGetOpen(login)

            if not isinstance(open_orders, list):
                raise Exception("Unable to fetch orders")

            for order in open_orders:
                self.__manager.OrderDelete(order.Order)

            return True
        except Exception as e:
            print(f"Error deleting pending orders: {str(e)}")
            return False

    def get_account_target(self, login: int) -> str:
        try:
            assert self.connected, "mt5_server must be connected"

            user = MT5Manager.MTUser(self.__manager)

            user: MT5Manager.MTUser = self.__manager.UserGet(login)

            if user is False:
                print(f"failed to get user")
            else:
                return user.LeadCampaign
        except Exception as e:
            print(f"Error getting account target: {str(e)}")
            return None

    def get_account_group(self, login: int) -> str:
        try:
            assert self.connected, "mt5_server must be connected"

            user = MT5Manager.MTUser(self.__manager)

            user: MT5Manager.MTUser = self.__manager.UserGet(login)

            if user is False:
                return None
            else:
                return user.Group
        except Exception as e:
            print(f"Error getting account group: {str(e)}")
            return None

    def activate_account(self, login: int) -> bool:
        try:
            assert self.connected, "mt5_server must be connected"

            user_obj = MT5Manager.MTUser(self.__manager)
            user_obj: MT5Manager.MTUser = self.__manager.UserGet(login)

            user_obj.Rights = (
                user_obj.Rights
                | MT5Manager.MTUser.EnUsersRights.USER_RIGHT_ENABLED
                | MT5Manager.MTUser.EnUsersRights.USER_RIGHT_EXPERT
            ) & (~MT5Manager.MTUser.EnUsersRights.USER_RIGHT_TRADE_DISABLED)

            user_obj.Color = 3329330

            response = self.__manager.UserUpdate(user_obj)

            if response != True:
                print("There was an error activating the user")
                return False
            else:
                return True
        except Exception as e:
            print(f"Error activating account: {str(e)}")
            return False

    def enable_account(self, login: int, initial_balance: float) -> bool:
        try:
            assert self.connected, "mt5_server must be connected"

            user_obj = MT5Manager.MTUser(self.__manager)
            user_obj: MT5Manager.MTUser = self.__manager.UserGet(login)
            user_obj.Company = str(initial_balance)

            user_obj.Rights = (
                user_obj.Rights
                | MT5Manager.MTUser.EnUsersRights.USER_RIGHT_ENABLED
                | MT5Manager.MTUser.EnUsersRights.USER_RIGHT_EXPERT
            ) & (~MT5Manager.MTUser.EnUsersRights.USER_RIGHT_TRADE_DISABLED)

            user_obj.Color = 3329330

            response = self.__manager.UserUpdate(user_obj)

            if response != True:
                print("There was an error enabling the user")
                return False
            else:
                return True
        except Exception as e:
            print(f"Error enabling account: {str(e)}")
            return False

    def get_account_status_data(self, login: int):
        try:
            assert self.connected, "mt5_server must be connected"

            user_obj = self.__manager.UserGet(login)

            user_acc = self.__manager.UserAccountGet(login)

            if not user_obj:
                print("error fetching user")

            activeAccount = not (
                (
                    user_obj.Rights
                    & MT5Manager.MTUser.EnUsersRights.USER_RIGHT_TRADE_DISABLED
                )
                > 0
            )

            profit = user_acc.Profit

            balance = user_obj.Balance

            equity = user_acc.Equity

            group = user_obj.Group

            yesterdayEquity = user_obj.EquityPrevDay

            return (activeAccount, profit, balance, equity, group, yesterdayEquity)

        except Exception as e:
            print(f"Error getting account status data: {str(e)}")
            return (None, None, None, None, None, None)

    def disable_account(self, login: int):
        try:
            assert self.connected, "mt5_server must be connected"

            user_obj = self.__manager.UserGet(login)

            user_obj.Rights = (
                user_obj.Rights
                | MT5Manager.MTUser.EnUsersRights.USER_RIGHT_TRADE_DISABLED
            )

            user_obj.Color = 255

            self.__manager.UserUpdate(user_obj)

            return True
        except Exception as e:
            print(f"Error disabling account: {str(e)}")
            return False

    def is_funded_group(self, group_name: str):
        try:
            assert self.connected, "mt5_server must be connected"

            with open("groups.json") as file:
                groups = json.loads(file.read())

                matching_groups = [
                    group for group in groups if group["group_name"] == group_name
                ]

                if not matching_groups:
                    return False

                group_info = matching_groups[0]

                return group_info["funded"]
        except Exception as e:
            print(f"Error checking if group is funded: {str(e)}")
            return False

    def delete_account(self, login: int):
        try:
            assert self.connected, "mt5_server must be connected"

            user_deleted = self.__manager.UserDelete(login)

            if not user_deleted:
                raise Exception("There was an issue deleting user account")

            return True
        except Exception as e:
            print(f"Error deleting account: {str(e)}")
            return False

    def reset_to_initial_balance(self, login: int, initial_balance: float) -> bool:
        try:
            assert self.connected, "mt5_server must be connected"

            user_account: MT5Manager.MTAccount = self.__manager.UserAccountGet(login)

            sink = DealerSink()

            request = MT5Manager.MTRequest(self.__manager)

            request.Action = MT5Manager.MTRequest.EnTradeActions.TA_DEALER_BALANCE

            request.Type = MT5Manager.MTOrder.EnOrderType.OP_SELL_STOP

            request.Login = login

            request.PriceOrder = initial_balance - user_account.Equity

            response = self.__manager.DealerSend(request, sink)

            return True
        except Exception as e:
            print(f"Error resetting to initial balance: {str(e)}")
            return False
