"""File containing interface classes modified for Discord Webhook."""

import requests
from pathlib import Path

class CallbacksAbstract:
    """Discord Webhookに通知を送信するためのコールバッククラス"""

    def __init__(self):
        # =================================================================
        # ★ ここにご自身のDiscord Webhook URLを貼り付けてください ★
        # =================================================================
        self.webhook_url = "https://discord.com/api/webhooks/1506181559332634624/lUW2_ZVIqhcwMHipf0VLx4zca0LUuUjru1IeEHnbg4rwhNzv5nB3JZDPZHlaX88fP1ZL"

    def _send_to_discord(self, text: str):
        """DiscordのWebhookにPOSTリクエストを送信する内部関数"""
        if self.webhook_url == "https://discord.com/api/webhooks/1506181559332634624/lUW2_ZVIqhcwMHipf0VLx4zca0LUuUjru1IeEHnbg4rwhNzv5nB3JZDPZHlaX88fP1ZL" or not self.webhook_url:
            print(f"[Discord設定待ち] {text}")
            return
        
        data = {"content": text}
        try:
            # タイムアウトを設定してプログラム全体が止まるのを防ぎます
            requests.post(self.webhook_url, json=data, timeout=5)
        except Exception as e:
            print(f"Discordへの送信に失敗しました: {e}")

    async def on_start(self):
        self._send_to_discord("🚀 **モニター起動**\nApple Storeの在庫監視を開始しました。")

    async def on_stop(self):
        self._send_to_discord("🛑 **モニター停止**\nApple Storeの在庫監視を停止しました。")

    async def on_stock_available(self, message):
        # メンション（通知音）を鳴らしたい場合は "@everyone " などを先頭に追加してください
        self._send_to_discord(f"🚨 **【在庫復活】**\n{message}")

    async def on_appointment_available(self, message):
        self._send_to_discord(f"📅 **【予約枠空きあり】**\n{message}")

    async def on_newly_available(self):
        # 新規の在庫があった場合の処理（必要に応じて追加）
        pass

    async def on_auto_report(self, report: str):
        # 定期レポート
        self._send_to_discord(f"📊 **【定期レポート】**\n{report}")

    async def on_proxy_depletion(self, message: str):
        # プロキシ警告（通知がうるさければ pass に変更してください）
        pass

    async def on_long_processing_warning(self, warning: str):
        # 処理遅延警告（通知がうるさければ pass に変更してください）
        pass

    async def on_connection_error(self, error: str):
        # 接続エラーは頻発する可能性があるため、Discordに送らずコンソール出力のみが無難です
        print(f"接続エラー: {error}")

    async def on_error(self, error: str, logfile_path: Path):
        self._send_to_discord(f"❌ **【エラー発生】**\n{error}\n詳細ログ: {logfile_path}")
