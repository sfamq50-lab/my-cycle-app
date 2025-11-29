import streamlit as st

def calculate_nutrition(weight, distance, elevation, intensity):
    # Coefficients based on intensity
    coefficients = {
        "ポタリング": 3.0,
        "トレーニング": 3.8,
        "レース": 4.5
    }
    
    coeff = coefficients.get(intensity, 3.0)
    
    # Calculate Base Burn
    base_burn = weight * distance * coeff
    
    # Calculate Climb Burn
    climb_burn = elevation * weight * 0.05
    
    # Total Calories
    total_kcal = base_burn + climb_burn
    
    # Required Carbs (g)
    # Total Kcal * 50% / 4 kcal/g
    carbs_g = (total_kcal * 0.5) / 4
    
    # Required Water (ml)
    # Proposed logic: Distance * 20ml
    water_ml = distance * 20
    
    return total_kcal, water_ml, carbs_g

def main():
    st.set_page_config(page_title="CycleFoodApp", page_icon="🚴")
    
    st.title("🚴 CycleFoodApp")
    st.markdown("サイクリングの消費カロリーと補給食の目安を計算します。")
    
    # User Inputs
    st.header("📝 走行データ入力")
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight = st.number_input("体重 (kg)", min_value=30.0, max_value=150.0, value=60.0, step=0.1)
        distance = st.number_input("走行距離 (km)", min_value=0.0, max_value=1000.0, value=50.0, step=1.0)
        
    with col2:
        elevation = st.number_input("獲得標高 (m)", min_value=0.0, max_value=10000.0, value=500.0, step=10.0)
        intensity = st.selectbox("強度レベル", ["ポタリング", "トレーニング", "レース"])
    
    # Calculate
    if st.button("計算する", type="primary"):
        total_kcal, water_ml, carbs_g = calculate_nutrition(weight, distance, elevation, intensity)
        
        st.divider()
        
        # Display Results
        st.header("📊 計算結果")
        
        r_col1, r_col2, r_col3 = st.columns(3)
        
        with r_col1:
            st.metric("総消費カロリー", f"{int(total_kcal)} kcal")
        with r_col2:
            st.metric("必要な水分量", f"{int(water_ml)} ml")
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
