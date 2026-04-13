import time
import datetime
from plyer import notification
import pandas as pd
from pathlib import Path
import logging
import argparse
import math

parser = argparse.ArgumentParser(description="商品データのバリデーションツール")
parser.add_argument("--max-weight", type=int, default=3000, help="重量の上限値（グラム）。デフォルト: 3000g")
args = parser.parse_args()

current_dir = Path(__file__).parent
log_path = current_dir / "app.log"



logging.basicConfig(
    filename=str(log_path),
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding="utf-8",
    force=True
)

logger = logging.getLogger(__name__)

MAX_WEIGHT_G = args.max_weight



def validate_item(item):
    logger.debug("チェック開始：%s", item['品名'])
    if item.get("値段") is None or math.isnan(item.get("値段")):
        logger.warning("価格未定の商品です：%s", item['品名'])
        return False
    if item.get("重さ") is None:
        logger.error("重量が設定されていません：%s", item['品名'])
        return False
    if item.get("重さ") >=MAX_WEIGHT_G:
        logger.error("重量オーバーを検知：%s (%dg)", item['品名'], item['重さ'])
        return False

        
    logger.info("チェック成功：%s", item['品名'])
    return True
    


csv_path = current_dir / "items.csv"
df_input = pd.read_csv(csv_path)
results = df_input.to_dict(orient="records")


total = len(results)
logger.info("調査プロジェクト開始　全%d件", total)

for i, item in enumerate(results,start=1):
    try:
        print(f"{total}件中　{i}件目を処理中・・・\n商品名：{item['品名']}")
        time.sleep(0.5)

        success = validate_item(item)
        if not success:
            print(f"【警告】{item['品名']} は基準を満たしません。詳細はログを確認。")
    except Exception:
        logger.error("予期せるエラー発生", exc_info=True)


notification.notify(
    title="completed",
    message=f"全{total}件の調査が完了しました。",
    timeout=5
)



today_date = datetime.date.today()
now_time = datetime.datetime.now()






file_name = "inspection_results.csv"

file_path = current_dir / file_name


df = pd.DataFrame(results)
df["調査日"] = today_date
df["調査日時"] = now_time.strftime("%Y-%m-%d %H:%M:%S")


if not file_path.exists():
    df.to_csv(file_path, encoding="utf-8-sig", index=False)
else:
    df.to_csv(file_path, mode="a", encoding="utf-8-sig", index=False, header=False) 






