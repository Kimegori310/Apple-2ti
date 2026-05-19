import asyncio
from monitor import Monitor
from interface import CallbacksAbstract
# config.tomlを読み込む処理が走るようにインポート
import confighandler 

async def main():
    print("Discord通知モードで起動します...")
    
    # 変更したDiscord用のコールバックを初期化
    callbacks = CallbacksAbstract()
    await callbacks.on_start()

    try:
        # モニター（監視システム）にコールバックを渡して起動
        # ※元のmonitor.pyの仕様に合わせていますが、もし引数エラーが出る場合は微調整が必要です
        app_monitor = Monitor(callbacks)
        await app_monitor.start()
        
        # 監視ループを維持
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        await callbacks.on_stop()
        print("終了します。")

if __name__ == "__main__":
    asyncio.run(main())
