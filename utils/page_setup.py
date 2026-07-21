"""
page_setup.py — shared sidebar styling & branding
Call inject_sidebar() at the top of every page (after set_page_config).
"""
import streamlit as st


_SIDEBAR_CSS = """
<style>
/* ════════════════════════════════════════════════
   SIDEBAR  — minimal dark glass panel
════════════════════════════════════════════════ */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b1623 0%, #080d16 60%, #050810 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
    min-width: 240px !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1rem;
}

[data-testid="stSidebarNav"] {
    padding: 0.5rem 0.8rem 1.2rem !important;
    background: transparent !important;
}

[data-testid="stSidebarNavLink"] {
    border-radius: 10px !important;
    padding: 0.62rem 1rem !important;
    margin-bottom: 0.18rem !important;
    color: #64748b !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    text-decoration: none !important;
    transition: background 0.2s ease, color 0.2s ease !important;
    border: 1px solid transparent !important;
}
[data-testid="stSidebarNavLink"]:hover {
    background: rgba(16,185,129,0.07) !important;
    color: #a7f3d0 !important;
    border-color: rgba(16,185,129,0.14) !important;
}

[data-testid="stSidebarNavLink"][aria-selected="true"] {
    background: rgba(16,185,129,0.11) !important;
    color: #34d399 !important;
    font-weight: 700 !important;
    border: 1px solid rgba(16,185,129,0.22) !important;
}

[data-testid="stSidebarNavLink"] img,
[data-testid="stSidebarNavLink"] svg {
    opacity: 0.55;
}
[data-testid="stSidebarNavLink"][aria-selected="true"] img,
[data-testid="stSidebarNavLink"][aria-selected="true"] svg {
    opacity: 1;
}

[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0 !important;
}

[data-testid="stSidebar"]::-webkit-scrollbar { width: 4px; }
[data-testid="stSidebar"]::-webkit-scrollbar-track { background: transparent; }
[data-testid="stSidebar"]::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 4px; }
</style>
"""


def inject_sidebar():
    """
    Inject global sidebar CSS and render a minimal branding header.
    Call this once at the top of every page (right after st.set_page_config).
    """
    st.markdown(_SIDEBAR_CSS, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("""
        <div style="
            margin: 0.5rem 0 1rem;
            padding: 1rem 1.1rem;
            background: rgba(16,185,129,0.06);
            border: 1px solid rgba(16,185,129,0.14);
            border-radius: 14px;
            text-align: center;
        ">
            <div style="font-size:1.7rem;margin-bottom:0.3rem;">🌿</div>
            <div style="
                font-size:0.92rem;
                font-weight:800;
                background: linear-gradient(135deg,#a7f3d0,#10b981);
                -webkit-background-clip:text;
                -webkit-text-fill-color:transparent;
                background-clip:text;
                letter-spacing:0.3px;
                line-height:1.25;
            ">Plant Disease<br>Detection</div>
            <div style="
                font-size:0.65rem;
                color:#334155;
                font-weight:600;
                text-transform:uppercase;
                letter-spacing:1.5px;
                margin-top:0.35rem;
            ">Deep Learning · v1.0</div>
        </div>
        """, unsafe_allow_html=True)