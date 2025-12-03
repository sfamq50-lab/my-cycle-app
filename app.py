import streamlit as st
import pandas as pd
from datetime import datetime

def calculate_nutrition(weight, distance, elevation, temperature, speed):
    # Coefficients and Rates based on Speed
    if speed < 20:
        coeff = 0.28
        carb_rate = 30.0
    elif 20 <= speed < 28:
        coeff = 0.33
        carb_rate = 50.0
    else: # >= 28
        coeff = 0.40
        carb_rate = 70.0
    
    # Calculate Duration (hours)
    if distance > 0 and speed > 0:
        duration_hours = distance / speed
    else:
        duration_hours = 0.0
        
    # Format Duration String
    hours = int(duration_hours)
    minutes = int((duration_hours - hours) * 60)
    time_str = f"{hours}時間{minutes}分"
    
    # Calculate Base Burn (Calories)
    base_burn = weight * distance * coeff
    
    # Calculate Climb Burn (Calories)
    climb_burn = weight * elevation * 0.006
    
    # Total Calories
    total_kcal = base_burn + climb_burn
    
    # Required Carbs (g)
    # Based on hourly rate
    carbs_g = duration_hours * carb_rate
    
    # Required Water (ml)
    # Based on temperature
    if temperature < 15:
        water_rate = 350
    elif 15 <= temperature < 25:
        water_rate = 500
    elif 25 <= temperature < 30:
        water_rate = 750
    else: # >= 30
        water_rate = 1000
        
    water_ml = duration_hours * water_rate
    
    return total_kcal, water_ml, carbs_g, time_str, duration_hours

def calculate_difficulty(distance, elevation):
    if distance == 0:
        return "平坦", "★☆☆☆", 0, "平坦基調です。いつものペースで走れます。"
        
    # Climb Coefficient = Elevation (m) / Distance (km)
    coeff = elevation / distance
    
    if coeff < 5:
        return "平坦", "★☆☆☆", 0, "平坦基調です。いつものペースで走れます。"
    elif 5 <= coeff < 10:
        return "丘陵", "★★☆☆", -2, "適度なアップダウンがあります。設定速度だと少しキツイかもしれません。"
    elif 10 <= coeff < 20:
        return "山岳", "★★★☆", -5, "本格的な登りを含みます。設定速度だとかなりキツイ可能性があります。"
    else: # >= 20
        return "激坂", "★★★★", -8, "過酷なコースです！無理のないペース配分を心がけてください。"

def main():
    st.set_page_config(
        page_title="CycleFuel - 補給プランナー",
        page_icon="🚴",
        layout="centered"
    )
    
    st.title("🚴 CycleFoodApp")
    st.markdown("サイクリングの消費カロリーと補給食の目安を計算します。")
    
    # Initialize session state variables if not present
    if 'weight' not in st.session_state: st.session_state.weight = 60.0
    if 'distance' not in st.session_state: st.session_state.distance = 50.0
    if 'elevation' not in st.session_state: st.session_state.elevation = 300
    if 'speed' not in st.session_state: st.session_state.speed = 22.0
    if 'temperature' not in st.session_state: st.session_state.temperature = 20.0
    if 'history' not in st.session_state: st.session_state.history = []
    
    # Callbacks for synchronization
    def update_weight_slider(): st.session_state.weight = st.session_state.weight_slider
    def update_weight_input(): st.session_state.weight = st.session_state.weight_input
    def update_dist_slider(): st.session_state.distance = st.session_state.dist_slider
    def update_dist_input(): st.session_state.distance = st.session_state.dist_input
    def update_elev_slider(): st.session_state.elevation = st.session_state.elev_slider
    def update_elev_input(): st.session_state.elevation = st.session_state.elev_input
    def update_speed_slider(): st.session_state.speed = st.session_state.speed_slider
    def update_speed_input(): st.session_state.speed = st.session_state.speed_input
    def update_temp_slider(): st.session_state.temperature = st.session_state.temp_slider
    def update_temp_input(): st.session_state.temperature = st.session_state.temp_input

    # User Inputs
    st.header("📝 走行データ入力")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Weight Sync
        w_col1, w_col2 = st.columns([0.7, 0.3])
        with w_col1:
            st.slider("体重 (kg)", 30.0, 100.0, key='weight_slider', value=st.session_state.weight, on_change=update_weight_slider, step=0.1)
        with w_col2:
            st.number_input("体重入力", 30.0, 100.0, key='weight_input', value=st.session_state.weight, on_change=update_weight_input, step=0.1, label_visibility="collapsed")
        
        # Distance Sync
        d_col1, d_col2 = st.columns([0.7, 0.3])
        with d_col1:
            st.slider("走行距離 (km)", 0.0, 300.0, key='dist_slider', value=st.session_state.distance, on_change=update_dist_slider)
        with d_col2:
            st.number_input("距離入力", 0.0, 300.0, key='dist_input', value=st.session_state.distance, on_change=update_dist_input, step=1.0, label_visibility="collapsed")
        
    with col2:
        # Elevation Sync
        e_col1, e_col2 = st.columns([0.7, 0.3])
        with e_col1:
            st.slider("獲得標高 (m)", 0, 3000, key='elev_slider', value=st.session_state.elevation, on_change=update_elev_slider, step=10, help="【獲得標高の目安 (100kmあたり)】\n\n・0〜300m: 平坦 (河川敷など)\n・500〜800m: 丘陵 (多摩湖・尾根幹)\n・1000m超: 山岳 (都民の森・峠)")
        with e_col2:
            st.number_input("標高入力", 0, 3000, key='elev_input', value=st.session_state.elevation, on_change=update_elev_input, step=10, label_visibility="collapsed")

        # Course Diagnosis
        label, stars, penalty, message = calculate_difficulty(st.session_state.distance, st.session_state.elevation)
        st.info(f"🚴 **コース診断: {stars} ({label})**\n\n💡 {message}")
        
        # Speed Sync
        s_col1, s_col2 = st.columns([0.7, 0.3])
        with s_col1:
            st.slider("平均速度 (km/h)", 10.0, 45.0, key='speed_slider', value=st.session_state.speed, on_change=update_speed_slider, step=1.0, help="【速度設定のヒント】\n\n・15〜20km/h: ポタリング / 激坂を含むコース\n・20〜25km/h: 信号の多い街中 / トレーニング\n・25km/h以上: 信号のない平坦路 / レース")
        with s_col2:
            st.number_input("速度入力", 10.0, 45.0, key='speed_input', value=st.session_state.speed, on_change=update_speed_input, step=0.5, label_visibility="collapsed")
            
        st.caption("※山岳コースの場合は速度を下げて設定してください")
        
        # Temperature Sync
        t_col1, t_col2 = st.columns([0.7, 0.3])
        with t_col1:
            st.slider("気温 (℃)", 0.0, 40.0, key='temp_slider', value=st.session_state.temperature, on_change=update_temp_slider, step=1.0, help="走行当日の予想最高気温、または平均気温を入力してください。水分量の計算に影響します。")
        with t_col2:
            st.number_input("気温入力", 0.0, 40.0, key='temp_input', value=st.session_state.temperature, on_change=update_temp_input, step=1.0, label_visibility="collapsed")
    
    # Calculate
    if st.button("計算する", type="primary"):
        total_kcal, water_ml, carbs_g, time_str, duration_hours = calculate_nutrition(st.session_state.weight, st.session_state.distance, st.session_state.elevation, st.session_state.temperature, st.session_state.speed)
        
        # Calculate Phase Allocations
        before_kcal = total_kcal * 0.2
        during_kcal = total_kcal * 0.6
        after_kcal = total_kcal * 0.2
        
        # Calculate Hourly Rates for During Ride
        if duration_hours > 0:
            hourly_kcal = during_kcal / duration_hours
            hourly_water = water_ml / duration_hours
        else:
            hourly_kcal = 0
            hourly_water = 0

        # Save to History
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_record = {
            "日時": current_time,
            "距離 (km)": st.session_state.distance,
            "獲得標高 (m)": st.session_state.elevation,
            "平均速度 (km/h)": st.session_state.speed,
            "総消費カロリー (kcal)": int(total_kcal),
            "必要水分量 (ml)": int(water_ml)
        }
        st.session_state.history.append(new_record)

        st.divider()
        
        # Summary Section
        st.header("📊 計算結果")
        
        s_col1, s_col2 = st.columns(2)
        with s_col1:
            st.metric("総消費カロリー", f"{int(total_kcal)} kcal")
        with s_col2:
            st.metric("予想走行時間", time_str)
            
        st.subheader("🍽️ 栄養プランカード")
        
        # Card 1: Before Ride
        with st.container(border=True):
            st.subheader("⚡ ライド前 (1〜2時間前)")
            onigiri_count = before_kcal / 180
            st.markdown(f"### {int(before_kcal)} kcal")
            st.markdown(f"**🍙 おにぎり 約 {onigiri_count:.1f} 個分**")
            st.caption("炭水化物中心 / 水分補給")
            st.write("エネルギーを充填しましょう。おにぎり、パン、バナナなどがおすすめです。")

        # Card 2: During Ride
        with st.container(border=True):
            st.subheader("🚴 ライド中 (1時間ごと)")
            gel_count_hourly = hourly_kcal / 100
            bottle_count_hourly = hourly_water / 500
            
            c2_col1, c2_col2 = st.columns(2)
            with c2_col1:
                st.markdown("**⚡ エネルギー**")
                st.markdown(f"### {int(hourly_kcal)} kcal")
                st.markdown(f"**ジェル 約 {gel_count_hourly:.1f} 本分**")
            with c2_col2:
                st.markdown("**💧 水分**")
                st.markdown(f"### {int(hourly_water)} ml")
                st.markdown(f"**ボトル 約 {bottle_count_hourly:.1f} 本分**")
            
            st.caption("エナジージェル / スポーツドリンク / 塩分タブレット")
            st.write("こまめな補給が重要です。喉が渇く前に飲み、空腹を感じる前に食べましょう。")

        # Card 3: After Ride
        with st.container(border=True):
            st.subheader("☕ ライド後 (30分以内)")
            chicken_count = after_kcal / 120
            st.markdown(f"### {int(after_kcal)} kcal")
            st.markdown(f"**🍗 サラダチキン 約 {chicken_count:.1f} 個分**")
            st.caption("タンパク質 / リカバリー食")
            st.write("リカバリーのゴールデンタイムです。プロテインやバランスの良い食事を摂りましょう。")

    # History Section
    if st.session_state.history:
        st.markdown("---")
        st.header("📝 計算履歴")
        
        # Create DataFrame and sort by newest first
        df_history = pd.DataFrame(st.session_state.history)
        df_history = df_history.iloc[::-1] # Reverse order
        
        st.dataframe(df_history, use_container_width=True)
        
        # CSV Download
        csv = df_history.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="CSVをダウンロード",
            data=csv,
            file_name='cycle_fuel_plan.csv',
            mime='text/csv',
        )

    st.markdown("---")
    st.write("🚴 アプリの感想や、欲しい機能があれば教えてください！将来のアップデートの参考にさせていただきます。")
    st.link_button("開発者にメッセージを送る", "https://forms.gle/isZ9S9jwhuZwc8rHA")

if __name__ == "__main__":
    main()
