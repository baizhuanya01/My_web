import streamlit as st
import json, os, datetime

NOTES_FILE = "notes.json"
st.set_page_config(layout="wide")

def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []

def update_and_save(notes_data):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes_data, f, ensure_ascii=False, indent=2)
    st.session_state.notes = notes_data

if "editing" not in st.session_state:
    st.session_state.editing = False

current_tab = st.radio(
    "选择页面", 
    ["忏悔间", "我想她了"], 
    horizontal=True, 
    label_visibility="collapsed"
)

st.title("Ocegret Archive")
st.write("晨峻，今天的你忏悔了吗。")

if "notes" not in st.session_state:
    st.session_state.notes = load_notes()
notes = st.session_state.notes

    
if current_tab == "忏悔间":
    st.write("这里是用来给你进行学习以及生活上的反思的。\n当然也可以把笔记传上来，我会保留这个区域的访问权限。")

    st.divider()

    idx = st.session_state.get("current_index", None)
    
    if st.session_state.editing == True:
        if idx is None:
            st.info("你的罪业正在每一秒的颓唐中持续累积.ing")
        else:
            new = (idx == -1)
            de_title = "" if new else notes[idx]["title"]
            de_content = "" if new else notes[idx]["content"]
            title = st.text_input("罪业",value=de_title,placeholder="请为罪业命名")
            content = st.text_area("悔恨",value=de_content,placeholder="向天使安安大人忏悔些什么吧...", height=400)

            if st.button("保存"):
                if new:
                    notes.append({
                        "title": title,
                        "content": content,
                        "date": datetime.datetime.now().strftime("%m/%d %H:%M"),
                        "comments": []
                    })
                    update_and_save(notes)
                    st.session_state.current_index = len(notes) - 1
                    st.session_state.editing = False
                    st.rerun()
                else:
                    notes[idx]["title"] = title
                    notes[idx]["content"] = content
                    notes[idx]["date"] = datetime.datetime.now().strftime("%m/%d %H:%M")
                    update_and_save(notes)
                    st.session_state.editing = False
                    st.rerun()
 
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
                    st.rerun()

            with col2:
                if st.button("赎罪", type="secondary"):
                    notes.pop(idx)
                    update_and_save(notes)
                    st.session_state.current_index = None
                    st.session_state.editing = False
                    st.rerun()

            st.divider()

            st.markdown("### ⚖追加审判⚖")
            if "comments" not in note or not isinstance(note["comments"], list) :
                note["comments"] = []

            for c in note["comments"]:
                with st.chat_message("user(zhanwei)"):
                    st.write(f"*{c['time']}*")
                    st.write(c["text"])
            with st.form("my_comment_form", clear_on_submit=True):
                c_text = st.text_input(label="评价罪业", placeholder="追加审判中~请对告解者作出评判吧", label_visibility="collapsed")
                
                col_1, col_2 = st.columns([1, 5])
                with col_1:
                    submit_comment = st.form_submit_button("审判")
            if submit_comment and c_text:
                new_c = {
                    "text": c_text,
                    "time": datetime.datetime.now().strftime("%m/%d %H:%M")
                }
                notes[idx]["comments"].append(new_c)
                update_and_save(notes)
                st.rerun()

if current_tab == "我想她了":
    st.write("这里是用来给你宣泄有关于她的情绪的，我会找办法把这里锁上只向你开放。")
    st.divider()

    idx = st.session_state.get("current_index", None)
    
with st.sidebar:
    if current_tab == "忏悔间":
        if st.button("新的告解"):
            st.session_state.current_index = -1
            st.session_state.editing = True
        
        if notes:
            options = [f"{n['title']} ({n['date']})" for n in notes]
            current_idx = st.session_state.get("current_index")
            safe_index = current_idx if (current_idx is not None and current_idx != -1) else 0
            selected_index = st.selectbox(
                "选择往日告解", 
                range(len(notes)), 
                format_func=lambda x: options[x],
                index=safe_index
            )

            if st.session_state.get("current_index") != selected_index:
                st.session_state.current_index = selected_index
                st.session_state.editing = False
                st.rerun()
    elif current_tab == "我想她了":
        selection = st.selectbox(label="有关于她",options=["点滴美好","她之于我","弥补承诺"])
    # elif current_tab == "小说":
    #     pass
