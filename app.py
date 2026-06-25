import streamlit as st

# Cấu hình trang web
st.set_page_config(page_title="APP CHO VAY ONLINE KHCN - THUY HOAI", layout="centered")

st.title("🏦 Ứng Dụng Xét Duyệt Khoản Vay")
st.write("Nhập các thông tin dưới đây để kiểm tra điều kiện vay vốn.")

st.markdown("---")

# Tạo 2 cột để giao diện gọn gàng hơn
col1, col2 = st.columns(2)

with col1:
    STV = st.number_input("Số tiền muốn vay (Triệu đồng):", min_value=0.0, value=100.0, step=10.0)
    TGV = st.number_input("Thời gian vay (Số năm):", min_value=0.1, value=5.0, step=1.0)
    LSV = st.number_input("Lãi suất cho vay (Số thập phân, ví dụ 0.1 cho 10%):", min_value=0.0, max_value=1.0, value=0.1, step=0.01)
    TN = st.number_input("Thu nhập hàng tháng (Triệu đồng/tháng):", min_value=0.0, value=30.0, step=5.0)

with col2:
    SNTGD = st.number_input("Số người trong gia đình (Người):", min_value=0, value=2, step=1)
    PTMC = st.number_input("Số tiền phải trả cho khoản vay cũ (Triệu đồng):", min_value=0.0, value=0.0, step=1.0)
    GTTSDB = st.number_input("Giá trị tài sản đảm bảo (Triệu đồng):", min_value=1.0, value=200.0, step=10.0)
    STKH = st.number_input("Số tuổi của khách hàng (Tuổi):", min_value=0, max_value=120, value=30, step=1)

CPSH = 5

st.markdown("---")

# Nút bấm để kích hoạt tính toán
if st.button("📊 Kiểm tra kết quả", type="primary"):
    
    # Tính toán các chỉ số (Bọc trong try-except để tránh lỗi chia cho 0 nếu nhập sai)
    try:
        PTMM = (STV / (TGV * 12)) + (STV * (LSV / 12))
        thu_nhap_rong = TN - (SNTGD * CPSH)
        
        if thu_nhap_rong <= 0:
            st.error("❌ Thu nhập không đủ bù đắp chi phí sinh hoạt tối thiểu của gia đình!")
        else:
            DTI = (PTMM + PTMC) / thu_nhap_rong
            LTV = STV / GTTSDB

            # Hiển thị kết quả chỉ số
            st.subheader("📈 Kết quả phân tích:")
            st.write(f"- **Chỉ số DTI:** `{DTI * 100:.2f}%` (Tiêu chuẩn: $\le$ 70%)")
            st.write(f"- **Chỉ số LTV:** `{LTV * 100:.2f}%` (Tiêu chuẩn: $\le$ 70%)")
            st.write(f"- **Tuổi khách hàng:** `{STKH}` tuổi (Tiêu chuẩn: 18 - 70 tuổi)")
            
            st.markdown("---")
            
            # Xét điều kiện cho vay
            if DTI <= 0.7 and LTV <= 0.7 and 18 <= STKH <= 70:
                st.success("🎉 **ĐƯỢC CHO VAY**")
            else:
                st.error("🚨 **KHÔNG ĐƯỢC CHO VAY**")
                
                # Gợi ý lý do từ chối
                st.markdown("**Lý do không đạt:**")
                if DTI > 0.7: st.write("- Chỉ số DTI vượt quá 70% (Áp lực trả nợ quá cao).")
                if LTV > 0.7: st.write("- Chỉ số LTV vượt quá 70% (Giá trị tài sản đảm bảo không đủ).")
                if STKH < 18 or STKH > 70: st.write("- Độ tuổi không nằm trong phạm vi quy định (18 - 70 tuổi).")
                
    except ZeroDivisionError:
        st.error("❌ Có lỗi xảy ra do nhập giá trị bằng 0 ở các mục tính toán (Thời gian vay hoặc Giá trị tài sản).")
