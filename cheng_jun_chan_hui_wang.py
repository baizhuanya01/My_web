import streamlit as st
import json, os, datetime

NOTES_FILE = "notes.json"

def load_notes():
    if not os.path.exists(NOTES_FILE): return []
    with open(NOTES_FILE, "r", encoding="utf-8") as f: return json.load(f)

def save_notes(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

if "editing" not in st.session_state: st.session_state.editing = False
if "current_index" not in st.session_state: st.session_state.current_index = None

st.title("Ocegret Archive")
st.write("晨峻，今天的你忏悔了吗。")

notes = load_notes()

# 侧边栏放在最前面
with st.sidebar:
    st.title("忏悔区")
    if st.button("+ 新的告解"):
        st.session_state.current_index = -1
        st.session_state.editing = True
        st.rerun()
    for i, note in enumerate(notes):
        if st.button(f"{note['title'][:10]}... {note['date']}", key=f"btn_{i}"):
            st.session_state.current_index = i
            st.session_state.editing = False
            st.rerun()

idx = st.session_state.current_index
ct = st.radio("选择页面", ["忏悔间", "我想她了"], horizontal=True, label_visibility="collapsed")

if ct == "忏悔间":
    if st.session_state.editing:
        # 【终极解决】：给每一个编辑状态分配唯一的 Key，彻底断绝缓存
        # new 时用 -1，修改时用 idx，key 永远唯一
        edit_key = f"edit_form_{idx}"
        with st.form(key=edit_key):
            # 获取原始值
            curr_title = "" if idx == -1 else notes[idx]["title"]
            curr_content = "" if idx == -1 else notes[idx]["content"]
            
            t = st.text_input("罪业", value=curr_title)
            c = st.text_area("悔恨", value=curr_content, height=400)
            
            if st.form_submit_button("保存"):
                if idx == -1:
                    notes.append({"title": t, "content": c, "date": datetime.datetime.now().strftime("%m/%d %H:%M"), "comments": []})
                else:
                    notes[idx].update({"title": t, "content": c, "date": datetime.datetime.now().strftime("%m/%d %H:%M")})
                save_notes(notes)
                st.session_state.editing = False
                st.rerun()
    elif idx is not None and idx != -1:
        note = notes[idx]
        st.subheader(note["title"])
        st.markdown(note["content"])
        st.caption(f"时间：{note['date']}")
        
        if st.button("悔改"):
            st.session_state.editing = True
            st.rerun()
        if st.button("赎罪"):
            notes.pop(idx)
            save_notes(notes)
            st.session_state.current_index = None
            st.rerun()
        
        st.divider()
        st.markdown("### ⚖追加审判⚖")
        for comment in note.get("comments", []):
            st.write(f"*{comment['time']}* - {comment['text']}")
        
        with st.form(key=f"comm_{idx}", clear_on_submit=True):
            txt = st.text_input("追加审判")
            if st.form_submit_button("发送"):
                if txt:
                    notes[idx]["comments"].append({"text": txt, "time": datetime.datetime.now().strftime("%m/%d %H:%M")})
                    save_notes(notes)
                    st.rerun()

# ================= 4. 其他页面 =================
if ct == "思念堂":
    st.write("这里是用来给你宣泄有关于她的情绪的，我会找办法把这里锁上只向你开放。")
