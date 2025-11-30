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
    st.set_page_config(page_title="CycleFoodApp", page_icon="🚴")
    
    st.title("🚴 CycleFoodApp")
    st.markdown("サイクリングの消費カロリーと補給食の目安を計算します。")
    
    # Initialize session state variables if not present
    if 'weight' not in st.session_state: st.session_state.weight = 60.0
    if 'distance' not in st.session_state: st.session_state.distance = 50.0
    if 'elevation' not in st.session_state: st.session_state.elevation = 300
    if 'speed' not in st.session_state: st.session_state.speed = 22.0
    
    # Callbacks for synchronization
    def update_weight_slider(): st.session_state.weight = st.session_state.weight_slider
    def update_weight_input(): st.session_state.weight = st.session_state.weight_input
    def update_dist_slider(): st.session_state.distance = st.session_state.dist_slider
    def update_dist_input(): st.session_state.distance = st.session_state.dist_input
    def update_elev_slider(): st.session_state.elevation = st.session_state.elev_slider
    def update_elev_input(): st.session_state.elevation = st.session_state.elev_input
    def update_speed_slider(): st.session_state.speed = st.session_state.speed_slider
    def update_speed_input(): st.session_state.speed = st.session_state.speed_input

    # User Inputs
    st.header("📝 走行データ入力")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Weight Sync
        st.subheader("体重 (kg)")
        w_col1, w_col2 = st.columns([0.7, 0.3])
        with w_col1:
            st.slider("体重スライダー", 30.0, 150.0, key='weight_slider', value=st.session_state.weight, on_change=update_weight_slider, step=0.1, label_visibility="collapsed")
        with w_col2:
            st.number_input("体重入力", 30.0, 150.0, key='weight_input', value=st.session_state.weight, on_change=update_weight_input, step=0.1, label_visibility="collapsed")
        
        # Distance Sync
        st.subheader("走行距離 (km)")
        d_col1, d_col2 = st.columns([0.7, 0.3])
        with d_col1:
            st.slider("距離スライダー", 0.0, 600.0, key='dist_slider', value=st.session_state.distance, on_change=update_dist_slider, label_visibility="collapsed")
        with d_col2:
            st.number_input("距離入力", 0.0, 600.0, key='dist_input', value=st.session_state.distance, on_change=update_dist_input, step=1.0, label_visibility="collapsed")
        
    with col2:
        # Elevation Sync
        st.subheader("獲得標高 (m)")
        e_col1, e_col2 = st.columns([0.7, 0.3])
        with e_col1:
            st.slider("標高スライダー", 0, 3000, key='elev_slider', value=st.session_state.elevation, on_change=update_elev_slider, step=10, label_visibility="collapsed", help="【獲得標高の目安 (100kmあたり)】\n\n・0〜300m: 平坦 (河川敷など)\n・500〜800m: 丘陵 (多摩湖・尾根幹)\n・1000m超: 山岳 (都民の森・峠)")
        with e_col2:
            st.number_input("標高入力", 0, 3000, key='elev_input', value=st.session_state.elevation, on_change=update_elev_input, step=10, label_visibility="collapsed")

        # Course Diagnosis
        label, stars, penalty, message = calculate_difficulty(st.session_state.distance, st.session_state.elevation)
        st.info(f"🚴 **コース診断: {stars} ({label})**\n\n💡 {message}")
        
        # Speed Sync
        st.subheader("平均速度 (km/h)")
        s_col1, s_col2 = st.columns([0.7, 0.3])
        with s_col1:
            st.slider("速度スライダー", 10.0, 45.0, key='speed_slider', value=st.session_state.speed, on_change=update_speed_slider, step=1.0, label_visibility="collapsed", help="【速度設定のヒント】\n\n・15〜20km/h: ポタリング / 激坂を含むコース\n・20〜25km/h: 信号の多い街中 / トレーニング\n・25km/h以上: 信号のない平坦路 / レース")
        with s_col2:
            st.number_input("速度入力", 10.0, 45.0, key='speed_input', value=st.session_state.speed, on_change=update_speed_input, step=0.5, label_visibility="collapsed")
            
        st.caption("※山岳コースの場合は速度を下げて設定してください")
        temperature = st.slider("気温 (℃)", min_value=0, max_value=40, value=20)
    
    # Calculate
    if st.button("計算する", type="primary"):
        total_kcal, water_ml, carbs_g, time_str = calculate_nutrition(st.session_state.weight, st.session_state.distance, st.session_state.elevation, temperature, st.session_state.speed)
        
        st.divider()
        
        # Display Results
        st.header("📊 計算結果")
        st.subheader(f"⏱️ 予想走行時間: {time_str}")
        
        r_col1, r_col2, r_col3 = st.columns(3)
        
        with r_col1:
            st.metric("総消費カロリー", f"{int(total_kcal)} kcal")
        with r_col2:
            st.metric("必要な水分量", f"{int(water_ml)} ml")
            if temperature >= 30:
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

if __name__ == "__main__":
    main()
