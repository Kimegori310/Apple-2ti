import asyncio
from monitor import Monitor
from interface import CallbacksAbstract

def main():
    print("🚀 Discord通知モードで常時監視を開始します...")
    callbacks = CallbacksAbstract()
    
    # 衝突を防ぐために、専用のループ（実行レーン）を用意
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # 起動通知を送信
    loop.run_until_complete(callbacks.on_start())

    try:
        # モニターの初期化と起動
        app_monitor = Monitor(callbacks)
        loop.run_until_complete(app_monitor.start())
        
        # 終了されないように待機し続ける
        while True:
            loop.run_until_complete(asyncio.sleep(3600))
            
    except KeyboardInterrupt:
        # Ctrl+Cで止めた時
        loop.run_until_complete(callbacks.on_stop())
        print("🛑 監視を停止しました。")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
