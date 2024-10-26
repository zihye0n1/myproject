import streamlit as st
pages = {
    "카테고리1" : [
        st.Page("./page/a.py", title="페이지1"),
        st.Page("./page/b.py", title="페이지2")
    ],
    "카테고리2" : [
        st.Page("./page/c.py", title="페이지3"),
        st.Page("./page/d.py", title="페이지4")
    ]
}
pg = st.navigation(pages)
pg.run()