import streamlit as st
import json, os, datetime

NOTES_FILE = "notes.json"

def load_notes():
    if not os.path.exists(NOTES_FILE):
        return[]
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_notes(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

if "editing" not in st.session_state:
    st.session_state.editing = False

st.title("Ocegret Archive")
st.write("晨峻，今天的你忏悔了吗。")

notes = load_notes()

ct = st.radio(
    "选择页面",["忏悔间", "我想她了"], 
    horizontal=True, 
    label_visibility="collapsed"
)

if ct == "忏悔间":
    st.write("这里是用来给你进行学习以及生活上的反思的。\n当然也可以把笔记传上来，我会保留这个区域的访问权限。")

    st.divider()

    # ================= 核心优化1：将侧边栏代码提前 =================
    # 把侧边栏移到顶部，这样点击时能瞬间更新状态，不用点两次
    with st.sidebar:
        st.sidebar.title("忏悔区")
        if st.button("+ 新的告解"):
            st.session_state.current_index = -1
            st.session_state.editing = True
            # 【杀手锏】点击新建时，直接往大脑(session)里强行注入“空记忆”
            st.session_state["edit_title"] = ""
            st.session_state["edit_content"] = ""
    
        for i, note in enumerate(notes):
            preview = note["title"][:15] if note["title"] else "无告解"
            if st.button(f"{preview}  \n{note['date']}", key=f"note_{i}"):
                st.session_state.current_index = i
                st.session_state.editing = False

    idx = st.session_state.get("current_index", None)

    # ================= 1. 编辑/新建模式 =================
    if st.session_state.editing == True:
        if idx is None:
            st.info("你的罪业正在每一秒的颓唐中持续累积.ing")
        else:
            new = (idx == -1)
            
            # 使用固定名字的表单，彻底避免动态 Key 带来的缓存吞数据问题
            with st.form(key="edit_confession_form"):
                # 这里去掉了坑人的 value=...，直接让输入框绑定专属的 key
                title = st.text_input("罪业", placeholder="请为罪业命名", key="edit_title")
                content = st.text_area("悔恨", placeholder="向天使安安大人忏悔些什么吧...", height=400, key="edit_content")
                
                submit_save = st.form_submit_button("停止")
                
                if submit_save:
                    if new:
                        notes.append({
                            "title": title,
                            "content": content,
                            "date": datetime.datetime.now().strftime("%m/%d %H:%M"),
                            "comments":[]
                        })
                        save_notes(notes)
                        st.session_state.current_index = len(notes) - 1
                    else:
                        notes[idx]["title"] = title
                        notes[idx]["content"] = content
                        notes[idx]["date"] = datetime.datetime.now().strftime("%m/%d %H:%M")
                        save_notes(notes)
                    
                    st.session_state.editing = False
                    st.rerun()

    # ================= 2. 展示/阅读模式 =================
    else:
        if idx is None:
            st.info("你的罪业正在每一秒的颓唐中持续累积.ing")
        else:
            note = notes[idx]
            
            st.subheader(note["title"])
            st.markdown(note["content"])
            st.caption(f"最后一次忏悔时间：{note['date']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("悔改"):
                    st.session_state.editing = True
                    st.session_state["edit_title"] = note["title"]
                    st.session_state["edit_content"] = note["content"]
                    st.rerun()

            with col2:
                if st.button("赎罪", type="secondary"):
                    notes.pop(idx)
                    save_notes(notes)
                    st.session_state.current_index = None
                    st.session_state.editing = False
                    st.rerun()

            st.divider()

            # ================= 3. 追加审判 =================
            st.markdown("### ⚖追加审判⚖")
            if "comments" not in note or not isinstance(note["comments"], list) :
                note["comments"] = []

            for c in note["comments"]:
                with st.chat_message("user"):
                    st.write(f"*{c['time']}*")
                    st.write(c["text"])
            
            with st.form(key=f"comment_form_{idx}", clear_on_submit=True):
                c_text = st.text_input(label="追加审判", placeholder="追加审判中~请对告解者作出评判吧", label_visibility="collapsed")
                submit_btn = st.form_submit_button("发送审判")
    
                if submit_btn and c_text:
                    new_c = {
                        "text": c_text,
                        "time": datetime.datetime.now().strftime("%m/%d %H:%M")
                    }
                    notes[idx]["comments"].append(new_c)
                    save_notes(notes)
                    st.rerun()

# ================= 4. 其他页面 =================
if ct == "思念堂":
    st.write("这里是用来给你宣泄有关于她的情绪的，我会找办法把这里锁上只向你开放。")
