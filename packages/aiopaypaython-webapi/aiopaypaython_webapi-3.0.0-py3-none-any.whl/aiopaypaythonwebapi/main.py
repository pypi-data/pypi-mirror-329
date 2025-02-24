import httpx
import datetime
from uuid import uuid4
from typing import NamedTuple

headers = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
}


class PayPayWebAPIError(Exception):
    pass


class PayPayWebAPINetWorkError(Exception):
    pass


class PayPayWebAPILoginError(Exception):
    pass


class PayPayWebAPI:
    def __init__(
        self,
        proxy: str = None,
    ):
        self.session = httpx.AsyncClient(proxy=proxy)

    async def initialize(
        self,
        phone: str = None,
        password: str = None,
        client_uuid: str = str(uuid4()).upper(),
        access_token: str = None,
    ):
        self.client_uuid = client_uuid
        self.phone = phone
        self.password = password
        if access_token:
            self.access_token = access_token
            self.session.cookies.set("token", access_token)
        elif phone:
            self.access_token = None
            payload = {
                "scope": "SIGN_IN",
                "client_uuid": self.client_uuid,
                "grant_type": "password",
                "username": self.phone,
                "password": self.password,
                "add_otp_prefix": True,
                "language": "ja",
            }

            login = await self.session.post(
                "https://www.paypay.ne.jp/app/v1/oauth/token",
                json=payload,
                headers=headers,
            )
            try:
                self.access_token = login.json()["access_token"]
            except:
                try:
                    if login.json()["response_type"] == "ErrorResponse":
                        raise PayPayWebAPILoginError(login.json())
                    else:
                        self.otp_prefix = login.json()["otp_prefix"]
                        self.otp_reference_id = login.json()["otp_reference_id"]
                except:
                    raise PayPayWebAPINetWorkError(login.text)

    async def login(self, otp: str):
        payload = {
            "scope": "SIGN_IN",
            "client_uuid": self.client_uuid,
            "grant_type": "otp",
            "otp_prefix": self.otp_prefix,
            "otp": otp,
            "otp_reference_id": self.otp_reference_id,
            "username_type": "MOBILE",
            "language": "ja",
        }

        login: dict[str, str] = (
            await self.session.post(
                "https://www.paypay.ne.jp/app/v1/oauth/token",
                json=payload,
                headers=headers,
            )
        ).json()
        try:
            self.access_token = login["access_token"]
        except:
            raise PayPayWebAPILoginError(login)

        return login

    async def resend_otp(self, otp_reference_id: str) -> dict:
        payload = {"add_otp_prefix": "true"}
        resend = (
            await self.session.post(
                f"https://www.paypay.ne.jp/app/v1/otp/mobile/resend/{otp_reference_id}",
                json=payload,
                headers=headers,
            )
        ).json()

        try:
            self.otp_prefix = resend["otp_prefix"]
            self.otp_reference_id = resend["otp_reference_id"]
        except:
            raise PayPayWebAPILoginError(resend)

        return resend

    async def get_balance(self):
        if not self.access_token:
            raise PayPayWebAPILoginError("まずはログインしてください")

        balance: dict[str, str] = (
            await self.session.get(
                "https://www.paypay.ne.jp/app/v1/bff/getBalanceInfo",
                headers=headers,
            )
        ).json()
        if balance["header"]["resultCode"] == "S0001":
            raise PayPayWebAPILoginError(balance)

        if balance["header"]["resultCode"] != "S0000":
            raise PayPayWebAPIError(balance)

        try:
            money = balance["payload"]["walletDetail"]["emoneyBalanceInfo"]["balance"]
        except:
            money = None

        class GetBalance(NamedTuple):
            money: int
            money_light: int
            all_balance: int
            useable_balance: int
            points: int
            raw: dict

        money_light = balance["payload"]["walletDetail"]["prepaidBalanceInfo"][
            "balance"
        ]
        all_balance = balance["payload"]["walletSummary"]["allTotalBalanceInfo"][
            "balance"
        ]
        useable_balance = balance["payload"]["walletSummary"][
            "usableBalanceInfoWithoutCashback"
        ]["balance"]
        points = balance["payload"]["walletDetail"]["cashBackBalanceInfo"]["balance"]

        return GetBalance(
            money, money_light, all_balance, useable_balance, points, balance
        )

    async def get_profile(self):
        if not self.access_token:
            raise PayPayWebAPILoginError("まずはログインしてください")

        profile: dict[str, str] = (
            await self.session.get(
                "https://www.paypay.ne.jp/app/v1/getUserProfile",
                headers=headers,
            )
        ).json()

        if profile["header"]["resultCode"] == "S0001":
            raise PayPayWebAPILoginError(profile)

        if profile["header"]["resultCode"] != "S0000":
            raise PayPayWebAPIError(profile)

        class GetProfile(NamedTuple):
            name: str
            external_user_id: str
            icon: str
            raw: dict

        name = profile["payload"]["userProfile"]["nickName"]
        external_user_id = profile["payload"]["userProfile"]["externalUserId"]
        icon = profile["payload"]["userProfile"]["avatarImageUrl"]

        return GetProfile(name, external_user_id, icon, profile)

    async def get_history(self) -> dict:
        if not self.access_token:
            raise PayPayWebAPILoginError("まずはログインしてください")

        history: dict[str, str] = (
            await self.session.get(
                "https://www.paypay.ne.jp/app/v2/bff/getPay2BalanceHistory",
                headers=headers,
            )
        ).json()
        if history["header"]["resultCode"] == "S0001":
            raise PayPayWebAPILoginError(history)

        if history["header"]["resultCode"] != "S0000":
            raise PayPayWebAPIError(history)

        return history

    async def link_check(self, url: str):
        if "https://" in url:
            url = url.replace("https://pay.paypay.ne.jp/", "")

        param = {"verificationCode": url}
        link_info: dict[str, str] = (
            await self.session.get(
                f"https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo",
                headers=headers,
                params=param,
            )
        ).json()

        if link_info["header"]["resultCode"] != "S0000":
            raise PayPayWebAPIError(link_info)

        class LinkInfo(NamedTuple):
            sender_name: str
            sender_external_id: str
            sender_icon: str
            order_id: str
            chat_room_id: str
            amount: int
            status: str
            money_light: int
            money: int
            has_password: bool
            raw: dict

        sender_name = link_info["payload"]["sender"]["displayName"]
        sender_external_id = link_info["payload"]["sender"]["externalId"]
        sender_icon = link_info["payload"]["sender"]["photoUrl"]
        order_id = link_info["payload"]["pendingP2PInfo"]["orderId"]
        chat_room_id = link_info["payload"]["message"]["chatRoomId"]
        amount = link_info["payload"]["pendingP2PInfo"]["amount"]
        status = link_info["payload"]["message"]["data"]["status"]
        money_light = link_info["payload"]["message"]["data"]["subWalletSplit"][
            "senderPrepaidAmount"
        ]
        money = link_info["payload"]["message"]["data"]["subWalletSplit"][
            "senderEmoneyAmount"
        ]
        has_password = link_info["payload"]["pendingP2PInfo"]["isSetPasscode"]

        return LinkInfo(
            sender_name,
            sender_external_id,
            sender_icon,
            order_id,
            chat_room_id,
            amount,
            status,
            money_light,
            money,
            has_password,
            link_info,
        )

    async def link_receive(
        self, url: str, password: str = None, link_info: dict = None
    ) -> dict:
        if not self.access_token:
            raise PayPayWebAPILoginError("まずはログインしてください")

        if "https://" in url:
            url = url.replace("https://pay.paypay.ne.jp/", "")

        if not link_info:
            param = {"verificationCode": url}
            link_info: dict[str, str] = (
                await self.session.get(
                    f"https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo",
                    headers=headers,
                    params=param,
                )
            ).json()
            if link_info["header"]["resultCode"] != "S0000":
                raise PayPayWebAPIError(link_info)

        if link_info["payload"]["orderStatus"] != "PENDING":
            raise PayPayWebAPIError(
                "すでに 受け取り / 辞退 / キャンセル されているリンクです"
            )

        if link_info["payload"]["pendingP2PInfo"]["isSetPasscode"] and password == None:
            raise PayPayWebAPIError("このリンクにはパスワードが設定されています")

        payload = {
            "verificationCode": url,
            "client_uuid": self.client_uuid,
            "requestAt": str(
                datetime.datetime.now(
                    datetime.timezone(datetime.timedelta(hours=9))
                ).strftime("%Y-%m-%dT%H:%M:%S+0900")
            ),
            "requestId": link_info["payload"]["message"]["data"]["requestId"],
            "orderId": link_info["payload"]["message"]["data"]["orderId"],
            "senderMessageId": link_info["payload"]["message"]["messageId"],
            "senderChannelUrl": link_info["payload"]["message"]["chatRoomId"],
            "iosMinimumVersion": "3.45.0",
            "androidMinimumVersion": "3.45.0",
        }

        if password:
            payload["passcode"] = password

        receive: dict[str, str] = (
            await self.session.post(
                "https://www.paypay.ne.jp/app/v2/p2p-api/acceptP2PSendMoneyLink",
                json=payload,
                headers=headers,
            )
        ).json()
        if receive["header"]["resultCode"] == "S0001":
            raise PayPayWebAPILoginError(receive)

        if receive["header"]["resultCode"] != "S0000":
            raise PayPayWebAPIError(receive)

        return receive

    async def link_reject(self, url: str, link_info: dict = None) -> dict:
        if not self.access_token:
            raise PayPayWebAPILoginError("まずはログインしてください")

        if not link_info:
            param = {"verificationCode": url}
            link_info: dict[str, str] = (
                await self.session.get(
                    f"https://www.paypay.ne.jp/app/v2/p2p-api/getP2PLinkInfo",
                    headers=headers,
                    params=param,
                )
            ).json()
            if link_info["header"]["resultCode"] != "S0000":
                raise PayPayWebAPIError(link_info)

        if link_info["payload"]["orderStatus"] != "PENDING":
            raise PayPayWebAPIError(
                "すでに 受け取り / 辞退 / キャンセル されているリンクです"
            )

        payload = {
            "requestAt": datetime.datetime.now(
                datetime.timezone(datetime.timedelta(hours=9))
            ).strftime("%Y-%m-%dT%H:%M:%S+0900"),
            "orderId": link_info["payload"]["pendingP2PInfo"]["orderId"],
            "verificationCode": url,
            "requestId": str(uuid4()).upper(),
            "senderMessageId": link_info["payload"]["message"]["messageId"],
            "senderChannelUrl": link_info["payload"]["message"]["chatRoomId"],
            "iosMinimumVersion": "3.45.0",
            "androidMinimumVersion": "3.45.0",
            "client_uuid": self.client_uuid,
        }

        reject: dict[str, str] = (
            await self.session.post(
                "https://www.paypay.ne.jp/app/v2/p2p-api/rejectP2PSendMoneyLink",
                json=payload,
                headers=headers,
            )
        ).json()
        if reject["header"]["resultCode"] == "S0001":
            raise PayPayWebAPILoginError(reject)

        if reject["header"]["resultCode"] != "S0000":
            raise PayPayWebAPIError(reject)

        return reject

    async def create_p2pcode(self):
        if not self.access_token:
            raise PayPayWebAPILoginError("まずはログインしてください")

        create_p2pcode: dict[str, str] = (
            await self.session.post(
                "https://www.paypay.ne.jp/app/v1/p2p-api/createP2PCode",
                headers=headers,
            )
        ).json()
        if create_p2pcode["header"]["resultCode"] == "S0001":
            raise PayPayWebAPILoginError(create_p2pcode)

        if create_p2pcode["header"]["resultCode"] != "S0000":
            raise PayPayWebAPIError(create_p2pcode)

        class P2PCode(NamedTuple):
            p2pcode: str
            raw: dict

        p2pcode = create_p2pcode["payload"]["p2pCode"]

        return P2PCode(p2pcode, create_p2pcode)

    async def create_paymentcode(
        self, method: str = "WALLET", method_id: str = "106177237"
    ) -> dict:
        if not self.access_token:
            raise PayPayWebAPILoginError("まずはログインしてください")

        payload = {
            "paymentMethodType": method,
            "paymentMethodId": method_id,
            "paymentCodeSessionId": str(uuid4()),
        }
        paymentcode = (
            await self.session.post(
                "https://www.paypay.ne.jp/app/v2/bff/createPaymentOneTimeCodeForHome",
                headers=headers,
                json=payload,
            )
        ).json()
        if paymentcode["header"]["resultCode"] == "S0001":
            raise PayPayWebAPILoginError(paymentcode)

        if paymentcode["header"]["resultCode"] != "S0000":
            raise PayPayWebAPIError(paymentcode)

        return paymentcode

    # 残念ながらエンドポイントから消えてしまった
    async def create_link(self, amount: int, password: str = None) -> None:
        raise PayPayWebAPIError("404 Not Found")

    async def send_money(self, amount: int, external_id: str) -> None:
        raise PayPayWebAPIError("404 Not Found")
