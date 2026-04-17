# %%
import streamlit as st
import random
import pandas as pd
import os

# 設定檔案名稱
DATA_FILE = "restaurants_v2.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE).to_dict('records')
    return [
        {"name": "元味屋", "price": 150, "rating": 4.5},
        {"name": "成大館", "price": 100, "rating": 4.0},
        {"name": "麥當勞", "price": 120, "rating": 4.2},
        {"name": "活力小廚", "price": 80, "rating": 4.3}
    ]

def save_data(data):
    pd.DataFrame(data).to_csv(DATA_FILE, index=False)

if 'restaurant_db' not in st.session_state:
    st.session_state.restaurant_db = load_data()

st.title("🍴 聰明美食挑選器")

# --- 第一部分：篩選與隨機抽選 ---
st.divider()
st.header("🎯 今天想花多少錢？")

# 讓使用者設定預算
budget = st.slider("設定你的預算上限 ($)", min_value=0, max_value=1000, value=200, step=10)

if st.button("符合預算的餐廳，抽一個！", type="primary"):
    # 【核心邏輯】：過濾符合預算的餐廳
    # 注意：確保 price 是數字型態進行比較
    filtered_list = [res for res in st.session_state.restaurant_db if int(res['price']) <= budget]
    
    if filtered_list:
        selected = random.choice(filtered_list)
        st.balloons()
        
        with st.container():
            st.markdown(f"### 🎊 推薦結果：**{selected['name']}**")
            c1, c2 = st.columns(2)
            c1.metric("價格", f"${selected['price']}")
            c2.metric("評分", f"⭐️ {selected['rating']}")
            
            map_url = f"https://www.google.com/maps/search/{selected['name']}"
            st.markdown(f"[📍 點我導航到 {selected['name']}]( {map_url} )")
    else:
        st.warning(f"哎呀！預算 ${budget} 以內找不到餐廳，要不要加一點預算？")

# --- 第二部分：新增餐廳資料 ---
st.divider()
st.header("📝 新增美食資料")

with st.form("add_form", clear_on_submit=True):
    new_name = st.text_input("餐廳名稱")
    c1, c2 = st.columns(2)
    # 使用 number_input 確保存入的是數字
    new_price = c1.number_input("平均消費 ($)", min_value=0, step=10, value=100)
    new_rating = c2.slider("推薦評分 (0.0-5.0)", 0.0, 5.0, 4.0, 0.1)
    
    submitted = st.form_submit_button("新增至資料庫")
    if submitted:
        if new_name:
            new_data = {"name": new_name, "price": int(new_price), "rating": float(new_rating)}
            st.session_state.restaurant_db.append(new_data)
            save_data(st.session_state.restaurant_db)
            st.success(f"✅ 已成功加入 {new_name}！")
            st.rerun()

# --- 第三部分：資料庫管理 ---
st.divider()
with st.expander("📂 查看目前所有口袋名單"):
    if st.session_state.restaurant_db:
        df = pd.DataFrame(st.session_state.restaurant_db)
        df.columns = ["餐廳名稱", "價格", "評價"]
        st.dataframe(df, use_container_width=True) # 使用可互動的表格
        
        if st.button("清空所有資料"):
            st.session_state.restaurant_db = []
            save_data([])
            st.rerun()


