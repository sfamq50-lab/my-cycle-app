import streamlit as st

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
    
    return total_kcal, water_ml, carbs_g, time_str

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
        page_title="CycleFuel - 補給食計算機",
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
            st.slider("体重 (kg)", 30.0, 150.0, key='weight_slider', value=st.session_state.weight, on_change=update_weight_slider, step=0.1)
        with w_col2:
            st.number_input("体重入力", 30.0, 150.0, key='weight_input', value=st.session_state.weight, on_change=update_weight_input, step=0.1, label_visibility="collapsed")
        
        # Distance Sync
        d_col1, d_col2 = st.columns([0.7, 0.3])
        with d_col1:
            st.slider("走行距離 (km)", 0.0, 600.0, key='dist_slider', value=st.session_state.distance, on_change=update_dist_slider)
        with d_col2:
            st.number_input("距離入力", 0.0, 600.0, key='dist_input', value=st.session_state.distance, on_change=update_dist_input, step=1.0, label_visibility="collapsed")
        
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
        total_kcal, water_ml, carbs_g, time_str = calculate_nutrition(st.session_state.weight, st.session_state.distance, st.session_state.elevation, st.session_state.temperature, st.session_state.speed)
        
        st.divider()
        
        # Display Results
        st.header("📊 計算結果")
        st.subheader(f"⏱️ 予想走行時間: {time_str}")
        
        r_col1, r_col2, r_col3 = st.columns(3)
        
        with r_col1:
            st.metric("総消費カロリー", f"{int(total_kcal)} kcal")
        with r_col2:
            st.metric("必要な水分量", f"{int(water_ml)} ml")
            if st.session_state.temperature >= 30:
                st.error("※熱中症に注意！多めに持ちましょう")
        with r_col3:
            st.metric("必要糖質量", f"{int(carbs_g)} g")
            
        st.subheader("🍙 補給食の目安")
        
        # Food conversion
        # Onigiri: ~40g carbs
        # Gel: ~25g carbs
        
        onigiri_count = carbs_g / 40
        gel_count = carbs_g / 25
        
        f_col1, f_col2 = st.columns(2)
        
        with f_col1:
            st.info(f"**おにぎり** (1個 糖質約40g)\n\n### {onigiri_count:.1f} 個分")
            
        with f_col2:
            st.warning(f"**エナジージェル** (1本 糖質約25g)\n\n### {gel_count:.1f} 本分")

    st.markdown("---")
    st.write("🚴 アプリの感想や、欲しい機能があれば教えてください！将来のアップデートの参考にさせていただきます。")
    st.link_button("開発者にメッセージを送る", "https://forms.gle/isZ9S9jwhuZwc8rHA")

if __name__ == "__main__":
    main()
