import streamlit as st
import pandas as pd
import logging
from pathlib import Path

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

def validate_item(item, max_weight):
    logger.debug("チェック開始：%s", item['品名'])
    if item.get("値段") is None:
        logger.warning("価格未定の商品です：%s", item['品名'])
        return False
    if item.get("重さ") is None:
        logger.error("重量データなし：%s", item['品名'])
        return False
    if item.get("重さ") >= max_weight:
        logger.error("重量オーバーを検知：%s (%dg)", item['品名'], item['重さ'])
        return False
    logger.info("チェック成功：%s", item['品名'])
    return True

st.title("商品バリデーションツール")

uploaded_file = st.file_uploader("CSVファイルをアップロード", type="csv")
max_weight = st.slider("重量上限（g）", min_value=100, max_value=10000, value=3000, step=100)

if uploaded_file and st.button("実行"):
    df = pd.read_csv(uploaded_file)
    df = df.where(pd.notna(df), None)
    results = df.to_dict(orient="records")

    df["結果"] = ["✅ OK" if validate_item(item, max_weight) else "❌ NG" for item in results]

    st.dataframe(df)

    csv = df.to_csv(index=False, encoding="utf-8-sig")
    st.download_button("結果をダウンロード", csv, "results.csv", "text/csv")