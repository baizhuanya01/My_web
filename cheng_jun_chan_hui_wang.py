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

if st.session_state.snow == True:
    st.snow()
    st.session_state.snow = False
if st.session_state.balloons == True:
    st.balloons()
    st.session_state.balloons = False

st.title("晨峻忏悔网")
st.write("晨峻，今天的你忏悔了吗。")

notes = load_notes()
with st.sidebar:
    st.sidebar.title("功能区")
    if st.button("+ 新建笔记"):
        st.session_state.current_index = -1
        st.session_state.editing = True
    
    for i, note in enumerate(notes):
        preview = note["title"][:15] if note["title"] else "空笔记"
        if st.button(f"{preview}  \n{note['date']}", key=f"note_{i}"):
            st.session_state.current_index = i
            st.session_state.editing = False

# add_selectbox = st.sidebar.selectbox(
#     "你想要什么？",
#     ("忏悔","和她的回忆", "随笔")
# )

tab1, tab2= st.tabs(["忏悔间", "我想她了"])
    
with tab1:
    "这里是用来给你进行学习以及生活上的反思的。\n当然也可以把笔记传上来，我会保留这个区域的访问权限。"

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
            # if not new:
            #     comment = st.text_area("审判", value=de_comments, placeholder="追加审判中~请对告解者作出评判吧", height=200)
            if st.button("保存"):
                if new:
                    notes.append({
                        "title": title,
                        "content": content,
                        "date": datetime.datetime.now().strftime("%m/%d %H:%M"),
                        "comment": []
                    })
                    save_notes(notes)
                    st.session_state.current_index = len(notes) - 1
                    st.session_state.snow =True
                    st.rerun()
                else:
                    notes[idx]["title"] = title
                    notes[idx]["content"] = content
                    notes[idx]["date"] = datetime.datetime.now().strftime("%m/%d %H:%M")
                    save_notes(notes)
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
                    save_notes(notes)
                    st.session_state.current_index = None
                    st.session_state.editing = False
                    st.session_state.balloons = True
                    st.rerun()

            st.divider()

            st.markdown("### ⚖追加审判⚖")
            if "comments" not in note or not isinstance(note["comments"], list) :
                note["comments"] = []

            for c in note["comments"]:
                with st.chat_message("user(zhanwei)"):
                    st.write(f"*{c["time"]}*")
                    st.write(c["text"])
            c_text = st.chat_input(placeholder="追加审判中~请对告解者作出评判吧", height=200)
            if c_text:
                new_c = {
                    "text": c_text,
                    "time": datetime.datetime.now().strftime("%m/%d %H:%M")
                }
                notes[idx]["comments"].append(new_c)
                save_notes(notes)
                st.rerun()
                

with tab2:
    "这里是用来给你宣泄有关于她的情绪的，我会找办法把这里锁上只向你开放。"
