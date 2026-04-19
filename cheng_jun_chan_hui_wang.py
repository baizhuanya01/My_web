import streamlit as st
import json, os, datetime

NOTES_FILE = "notes.json"

def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
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
    "选择页面", 
    ["忏悔间", "思念堂"], 
    horizontal=True, 
    label_visibility="collapsed"
)
if ct == "忏悔间":
    st.write("这里是用来给你进行学习以及生活上的反思的。\n当然也可以把笔记传上来，我会保留这个区域的访问权限。")

    st.divider()

    idx = st.session_state.get("current_index", None)

# ================= 1. 编辑/新建模式 =================
    if st.session_state.editing == True:
        if idx is None:
            st.info("你的罪业正在每一秒的颓唐中持续累积.ing")
        else:
            new = (idx == -1)
            de_title = "" if new else notes[idx]["title"]
            de_content = "" if new else notes[idx]["content"]
            
            # 【核心修复】：为新建和每篇旧日记动态生成独一无二的表单 Key
            # 如果是新建，提交后自动清空缓存 (clear_on_submit=True)
            form_key = "form_new" if new else f"form_edit_{idx}"
            
            with st.form(key=form_key, clear_on_submit=new):
                # 输入框也必须加上动态的 key，彻底隔绝组件缓存污染
                title = st.text_input("罪业", value=de_title, placeholder="请为罪业命名", key=f"title_{form_key}")
                content = st.text_area("悔恨", value=de_content, placeholder="向天使安安大人忏悔些什么吧...", height=400, key=f"content_{form_key}")
                
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
                    
                    st.session_state.editing = False # 保存后自动退出编辑模式
                    st.rerun()

    # ================= 2. 展示/阅读模式 =================
    else:
        if idx is None:
            st.info("你的罪业正在每一秒的颓唐中持续累积.ing")
        else:
            note = notes[idx]
            
            # --- 告解正文展示区 ---
            st.subheader(note["title"])
            st.markdown(note["content"]) # 这里就是展示正文的代码
            st.caption(f"最后一次忏悔时间：{note['date']}")
            
            # --- 按钮操作区 ---
            col1, col2 = st.columns(2)
            with col1:
                if st.button("悔改"):
                    st.session_state.editing = True
                    st.rerun()

            with col2:
                if st.button("赎罪", type="secondary"):
                    notes.pop(idx)
                    save_notes(notes)
                    st.session_state.current_index = None
                    st.session_state.editing = False
                    st.rerun()

            st.divider()

            # --- 评论区及追加审判 ---
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

    # ================= 3. 侧边栏 =================
    with st.sidebar:
        st.sidebar.title("忏悔区")
        if st.button("+ 新的告解"):
           st.session_state.current_index = -1
           st.session_state.editing = True
    
        for i, note in enumerate(notes):
            preview = note["title"][:15] if note["title"] else "无告解"
            if st.button(f"{preview}  \n{note['date']}", key=f"note_{i}"):
                st.session_state.current_index = i
                st.session_state.editing = False

# ================= 4. 其他页面 =================
if ct == "思念堂":
    st.write("这里是用来给你宣泄有关于她的情绪的，我会找办法把这里锁上只向你开放。")
