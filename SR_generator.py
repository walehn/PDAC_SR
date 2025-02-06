import tkinter as tk
from tkinter import ttk
import pandas as pd
import os

# Initialize the main window
root = tk.Tk()
root.title("PDAC NCCN Structured Report Generator")

# Pt_counter 변수 초기화
Pt_counter = 1

# 모든 라디오버튼을 "Not provided"로 설정하는 함수
def reset_radio_buttons():
    global Pt_counter
    # 라디오버튼 변수들을 "Not provided"로 설정
    appearance_var.set("Not provided")
    size_var.set("Not provided")
    location_var.set("Not provided")
    pd_var.set("Not provided")
    biliary_var.set("Not provided")
    SMA_var.set("Not provided")
    celiac_var.set("Not provided")
    cha_var.set("Not provided")
    mpv_var.set("Not provided")
    smv_var.set("Not provided")
    liver_lesions_var.set("Not provided")
    nodules_var.set("Not provided")
    ascites_var.set("Not provided")
    lymph_nodes_var.set("Not provided")
    other_disease_var.set("Not provided")
    resect_var.set("Not Assessable")

    # 'Suspicious lymph nodes' 섹션의 체크박스들 초기화
    for var in lymph_node_vars:
        var.set(False)

    # 'Suspicious lymph nodes' 체크박스들을 포함하는 프레임 숨김
    if 'lymph_nodes_frame' in globals() and 'checkbox_frame' in globals():
        checkbox_frame.pack_forget()

    # Entry 위젯과 관련된 변수들을 초기화
    measure_entry.delete(0, tk.END)
    organ_involved_entry.delete(0, tk.END)
    
    # 추가적인 선택 옵션들을 초기화
    degree_var.set("")
    celiac_degree_var.set("")
    cha_degree_var.set("")
    mpv_degree_var.set("")
    smv_degree_var.set("")
    mpv_focal_var.set(False)
    smv_focal_var.set(False)

    # 선택 옵션 프레임을 숨김
    if 'measure_frame' in globals():
        measure_frame.pack_forget()
    if 'degree_frame' in globals():
        degree_frame.pack_forget()
    if 'celiac_degree_frame' in globals():
        celiac_degree_frame.pack_forget()
    if 'cha_degree_frame' in globals():
        cha_degree_frame.pack_forget()
    if 'mpv_degree_frame' in globals():
        mpv_degree_frame.pack_forget()
    if 'smv_degree_frame' in globals():
        smv_degree_frame.pack_forget()
    if 'organ_involved_frame' in globals():
        organ_involved_frame.pack_forget()

    # Pt_counter를 1 증가
    Pt_counter += 1
#    print(f"Pt_counter: {Pt_counter:03d}")  # 콘솔 로그에 Pt_counter 출력
    # status_label에 새로운 메시지 출력
    status_label.config(text=f"Patient {Pt_counter:03d} is ready.")

# 윈도우 크기 설정
window_width = 1024
window_height = 1260

# 스크린 너비와 높이 가져오기
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 윈도우를 화면 가운데에 배치하기 위한 x, y 좌표 계산
center_x = int((screen_width/2) - (window_width/2))
center_y = int((screen_height/2) - (window_height/2))

# 윈도우의 시작 위치 설정
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# Create a main frame
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

# Create a canvas
my_canvas = tk.Canvas(main_frame)
my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Add a scrollbar to the canvas
my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

# Create another frame inside the canvas
second_frame = tk.Frame(my_canvas)

# Add that new frame to a window in the canvas
my_canvas.create_window((0,0), window=second_frame, anchor="nw")

# Create two frames inside the second_frame for two-column layout
left_column = tk.Frame(second_frame)
right_column = tk.Frame(second_frame)

# Pack the columns inside the second_frame
left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Function to be called when OK button is pressed
def create_report():
    # 체크된 림프 노드의 항목을 가져오기
    checked_lymph_nodes = [detail for detail, var in zip(lymph_node_details, lymph_node_vars) if var.get()]
    lymph_nodes_result = "Present: " + ", ".join(checked_lymph_nodes) if lymph_nodes_var.get() == "Present" and checked_lymph_nodes else lymph_nodes_var.get()
    
    # MPV와 SMV 섹션에서 'Focal vessel narrowing or contour irregularity' 옵션 처리
    mpv_focal_result = "Positive focal vessel narrowing or contour irregularity" if mpv_focal_var.get() else ""
    smv_focal_result = "Positive Focal vessel narrowing or contour irregularity" if smv_focal_var.get() else ""

    # 각 subsection에서 선택된 값을 저장할 딕셔너리
    report_data = {
        "1-1 Appearance": appearance_var.get(),
        "1-2 Size": size_var.get() if size_var.get() != "Measurable" else f"Measurable: {measure_entry.get()} cm",
        "1-3 Location": location_var.get(),
        "1-4 Pancreatic duct": pd_var.get(),
        "1-5 Biliary tree": biliary_var.get(),
        "2-1 SMA Contact": SMA_var.get() if SMA_var.get() != "Present" else f"Present: {degree_var.get()}",
        "2-2 Celiac Axis Contact": celiac_var.get() if celiac_var.get() != "Present" else f"Present: {celiac_degree_var.get()}",
        "2-3 CHA Contact": cha_var.get() if cha_var.get() != "Present" else f"Present: {cha_degree_var.get()}",
        "3-1 MPV Contact": mpv_var.get() if mpv_var.get() != "Present" else f"Present: {mpv_degree_var.get()}, {mpv_focal_result}".strip(', '),
        "3-2 SMV Contact": smv_var.get() if smv_var.get() != "Present" else f"Present: {smv_degree_var.get()}, {smv_focal_result}".strip(', '),
        "4-1 Liver lesions": liver_lesions_var.get(),
        "4-2 Peritoneal or omental nodules": nodules_var.get(),
        "4-3 Ascites": ascites_var.get(),
        "4-4 Suspicious lymph nodes": lymph_nodes_result,
        "4-5 Other extrapancreatic disease": other_disease_var.get() if other_disease_var.get() != "Present" else f"Present: {organ_involved_entry.get()}",
        "5-1 Resectability": resect_var.get(),
    }
    # 엑셀 파일 경로
    filename = 'radiologist_SR_report.xlsx'

    # 데이터 프레임 생성
    new_df = pd.DataFrame([report_data])
    
    # 파일이 이미 존재하는지 확인
    if os.path.exists(filename):
        # 엑셀 파일 읽기 (index_col=None을 사용하여 기존 인덱스 무시)
        existing_df = pd.read_excel(filename, index_col=None)
        
        # 새 데이터프레임을 기존 데이터프레임에 추가
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        
        # 업데이트된 데이터프레임을 엑셀 파일로 저장
        updated_df.to_excel(filename, index=False)
    else:
        # 파일이 존재하지 않는 경우, 새 파일로 저장
        new_df.to_excel(filename, index=False)

    # 상태 메시지 업데이트
    status_label.config(text=f"Pt {Pt_counter:03d} structured report is created.")


# Frame for the Morphologic Evaluation section
style = ttk.Style()
style.configure("Bold.TLabelframe.Label", font=('Arial', 14, 'bold'))
#morphologic_frame = ttk.LabelFrame(second_frame, text="1. Morphologic Evaluation", style="Bold.TLabelframe")
#morphologic_frame.pack(fill="x", expand="yes", padx=10, pady=5)
morphologic_frame = ttk.LabelFrame(left_column, text="1. Morphologic Evaluation", style="Bold.TLabelframe")
morphologic_frame.pack(fill="x", expand=True, padx=10, pady=5)

# Appearance subsection
appearance_label = ttk.Label(morphologic_frame, text="1-1. Appearance (in the pancreatic parenchymal phase)")
appearance_label.pack(anchor="w")
appearance_options = ["Hypoattenuating", "Isoattenuating", "Hyperattenuating", "Not provided"]
appearance_var = tk.StringVar(value="Not provided")  # default value
for option in appearance_options:
    ttk.Radiobutton(morphologic_frame, text=option, variable=appearance_var, value=option).pack(anchor="w")

# Size subsection
size_frame = ttk.LabelFrame(morphologic_frame, text="1-2. Size (maximal axial dimension in centimeters)")
size_frame.pack(fill="x", expand="yes", padx=10, pady=5)

# Text entry for measurement (cm), initially not visible
measure_frame = tk.Frame(size_frame)
measure_label = ttk.Label(measure_frame, text="Measurment (cm):")
measure_entry = ttk.Entry(measure_frame, width=50)

size_var = tk.StringVar(value="Not provided")

def handle_size_selection():
    if size_var.get() == "Measurable":
        measure_label.pack(side="left")
        measure_entry.pack(side="left", fill="x", expand=True)
        measure_frame.pack(fill="x", expand=True, after=measurable_other_rb)
    else:
        measure_label.pack_forget()
        measure_entry.pack_forget()
        measure_frame.pack_forget()
        measure_entry.delete(0, tk.END)

# Radio buttons for size
measurable_other_rb = ttk.Radiobutton(size_frame, text="Measurable", variable=size_var, value="Measurable",
                         command=handle_size_selection)
measurable_other_rb.pack(anchor="w")

nonmeasurable_other_rb = ttk.Radiobutton(size_frame, text="Nonmeasurable (isoattenuating tumors)", variable=size_var, value="Nonmeasurable (isoattenuating tumors)",
                         command=handle_size_selection)
nonmeasurable_other_rb.pack(anchor="w")

size_not_provided_other_rb = ttk.Radiobutton(size_frame, text="Not provided", variable=size_var, value="Not provided",
                         command=handle_size_selection)
size_not_provided_other_rb.pack(anchor="w")


# Location subsection
location_label = ttk.Label(morphologic_frame, text="1-3. Location")
location_label.pack(anchor="w")
location_options = ["Head/uncinate (right of SMV)", "Neck (anterior to SMV/PV confluence)", "Body/tail (left of SMV)", "Not provided"]
location_var = tk.StringVar(value="Not provided")  # default value
for option in location_options:
    ttk.Radiobutton(morphologic_frame, text=option, variable=location_var, value=option).pack(anchor="w")

# pancreatic duct subsection
pd_label = ttk.Label(morphologic_frame, text="1-4. Pancreatic duct narrowing/abrupt cutoff with or without upstream dilatation")
pd_label.pack(anchor="w")
pd_options = ["Present", "Absent", "Not provided"]
pd_var = tk.StringVar(value="Not provided")  # default value
for option in pd_options:
    ttk.Radiobutton(morphologic_frame, text=option, variable=pd_var, value=option).pack(anchor="w")

# biliary tree duct subsection
biliary_label = ttk.Label(morphologic_frame, text="1-5. Biliary tree abrupt cutoff with or without upstream dilatation")
biliary_label.pack(anchor="w")
biliary_options = ["Present", "Absent", "Not provided"]
biliary_var = tk.StringVar(value="Not provided")  # default value
for option in biliary_options:
    ttk.Radiobutton(morphologic_frame, text=option, variable=biliary_var, value=option).pack(anchor="w")

# Frame for the Arterial Evaluation section
#arterial_frame = ttk.LabelFrame(second_frame, text="2. Arterial Evaluation", style="Bold.TLabelframe")
#arterial_frame.pack(fill="x", expand="yes", padx=10, pady=5)
arterial_frame = ttk.LabelFrame(left_column, text="2. Arterial Evaluation", style="Bold.TLabelframe")
arterial_frame.pack(fill="x", expand=True, padx=10, pady=5)

# SMA Contact 선택을 위한 Frame 생성 및 패킹
sma_contact_frame = tk.Frame(arterial_frame)
sma_contact_frame.pack(fill="x")

SMA_label = ttk.Label(sma_contact_frame, text="2-1. SMA Contact")
SMA_label.pack(anchor="w", side=tk.TOP)

SMA_var = tk.StringVar(value="Not provided")
degree_var = tk.StringVar(value="")

# Degree 선택 옵션
degree_options = ["≤ 180°", "> 180°"]

# Degree of solid soft-tissue contact 선택을 위한 Frame (초기엔 숨겨짐)
degree_frame = tk.Frame(sma_contact_frame)

def update_degree_visibility():
    if SMA_var.get() == "Present":
        degree_frame.pack(fill="x", expand=True,after=SMA_rb)  # Present 선택시 degree_frame을 패킹
        for widget in degree_frame.winfo_children():
            widget.destroy()  # 기존에 패킹된 위젯들을 제거
        for option in degree_options:
            ttk.Radiobutton(degree_frame, text=option, variable=degree_var, value=option).pack(anchor="w", padx=20)
    else:
        degree_frame.pack_forget()  # Absent/Not provided 선택시 degree_frame을 숨김
        degree_var.set("")

# SMA Contact 옵션 라디오버튼 패킹
SMA_rb = ttk.Radiobutton(sma_contact_frame, text="Present", variable=SMA_var, value="Present",command=update_degree_visibility)
SMA_rb.pack(anchor="w")

SMA2_rb = ttk.Radiobutton(sma_contact_frame, text="Absent", variable=SMA_var, value="Absent",command=update_degree_visibility)
SMA2_rb.pack(anchor="w")
SMA_not_provided_rb = ttk.Radiobutton(sma_contact_frame, text="Not provided", variable=SMA_var, value="Not provided", command=update_degree_visibility)
SMA_not_provided_rb.pack(anchor="w")


# Celiac Axis Contact 선택을 위한 Frame 생성 및 패킹
celiac_contact_frame = tk.Frame(arterial_frame)
celiac_contact_frame.pack(fill="x")

celiac_label = ttk.Label(celiac_contact_frame, text="2-2. Celiac Axis Contact")
celiac_label.pack(anchor="w", side=tk.TOP)

celiac_var = tk.StringVar(value="Not provided")
celiac_degree_var = tk.StringVar(value="")

# Degree 선택 옵션
celiac_degree_options = ["≤ 180°", "> 180°"]

# Degree of solid soft-tissue contact 선택을 위한 Frame (초기엔 숨겨짐)
celiac_degree_frame = tk.Frame(celiac_contact_frame)

def update_celiac_degree_visibility():
    if celiac_var.get() == "Present":
        celiac_degree_frame.pack(fill="x", expand=True, after=celiac_rb)  # Present 선택시 celiac_degree_frame을 패킹
        for widget in celiac_degree_frame.winfo_children():
            widget.destroy()  # 기존에 패킹된 위젯들을 제거
        for option in celiac_degree_options:
            ttk.Radiobutton(celiac_degree_frame, text=option, variable=celiac_degree_var, value=option).pack(anchor="w", padx=20)
    else:
        celiac_degree_frame.pack_forget()  # Absent/Not provided 선택시 celiac_degree_frame을 숨김
        celiac_degree_var.set("")

# Celiac Axis Contact 옵션 라디오버튼 패킹
celiac_rb = ttk.Radiobutton(celiac_contact_frame, text="Present", variable=celiac_var, value="Present", command=update_celiac_degree_visibility)
celiac_rb.pack(anchor="w")

celiac2_rb = ttk.Radiobutton(celiac_contact_frame, text="Absent", variable=celiac_var, value="Absent", command=update_celiac_degree_visibility)
celiac2_rb.pack(anchor="w")

celiac_not_provided_rb = ttk.Radiobutton(celiac_contact_frame, text="Not provided", variable=celiac_var, value="Not provided", command=update_celiac_degree_visibility)
celiac_not_provided_rb.pack(anchor="w")


# CHA Contact 선택을 위한 Frame 생성 및 패킹
cha_contact_frame = tk.Frame(arterial_frame)
cha_contact_frame.pack(fill="x")

cha_label = ttk.Label(cha_contact_frame, text="2-3. CHA Contact")
cha_label.pack(anchor="w", side=tk.TOP)

cha_var = tk.StringVar(value="Not provided")
cha_degree_var = tk.StringVar(value="")

# Degree 선택 옵션
cha_degree_options = ["≤ 180°", "> 180°"]

# Degree of solid soft-tissue contact 선택을 위한 Frame (초기엔 숨겨짐)
cha_degree_frame = tk.Frame(cha_contact_frame)

def update_cha_degree_visibility():
    if cha_var.get() == "Present":
        cha_degree_frame.pack(fill="x", expand=True, after=cha_rb)  # Present 선택시 cha_degree_frame을 패킹
        for widget in cha_degree_frame.winfo_children():
            widget.destroy()  # 기존에 패킹된 위젯들을 제거
        for option in cha_degree_options:
            ttk.Radiobutton(cha_degree_frame, text=option, variable=cha_degree_var, value=option).pack(anchor="w", padx=20)
    else:
        cha_degree_frame.pack_forget()  # Absent/Not provided 선택시 cha_degree_frame을 숨김
        cha_degree_var.set("")

# CHA Contact 옵션 라디오버튼 패킹
cha_rb = ttk.Radiobutton(cha_contact_frame, text="Present", variable=cha_var, value="Present", command=update_cha_degree_visibility)
cha_rb.pack(anchor="w")

cha2_rb = ttk.Radiobutton(cha_contact_frame, text="Absent", variable=cha_var, value="Absent", command=update_cha_degree_visibility)
cha2_rb.pack(anchor="w")

cha_not_provided_rb = ttk.Radiobutton(cha_contact_frame, text="Not provided", variable=cha_var, value="Not provided", command=update_cha_degree_visibility)
cha_not_provided_rb.pack(anchor="w")


# Frame for the Venous Evaluation section
#venous_frame = ttk.LabelFrame(second_frame, text="3. Venous Evaluation", style="Bold.TLabelframe")
#venous_frame.pack(fill="x", expand="yes", padx=10, pady=5)
venous_frame = ttk.LabelFrame(left_column, text="3. Venous Evaluation", style="Bold.TLabelframe")
venous_frame.pack(fill="x", expand=True, padx=10, pady=5)

# MPV Contact 선택을 위한 Frame 생성 및 패킹
mpv_contact_frame = tk.Frame(venous_frame)
mpv_contact_frame.pack(fill="x")

mpv_label = ttk.Label(mpv_contact_frame, text="3-1. MPV Contact")
mpv_label.pack(anchor="w", side=tk.TOP)

mpv_var = tk.StringVar(value="Not provided")
mpv_degree_var = tk.StringVar(value="")
mpv_focal_var = tk.BooleanVar(value=False)

# Degree와 Focal 선택 옵션
mpv_degree_options = ["≤ 180°", "> 180°"]
mpv_focal_option = "Focal vessel narrowing or contour irregularity"

# Degree와 Focal 선택을 위한 Frame (초기엔 숨겨짐)
mpv_degree_frame = tk.Frame(mpv_contact_frame)

def update_mpv_visibility():
    if mpv_var.get() == "Present":
        mpv_degree_frame.pack(fill="x", expand=True, after=mpv_rb)  # Present 선택시 mpv_degree_frame을 패킹
        for widget in mpv_degree_frame.winfo_children():
            widget.destroy()  # 기존에 패킹된 위젯들을 제거
        for option in mpv_degree_options:
            ttk.Radiobutton(mpv_degree_frame, text=option, variable=mpv_degree_var, value=option).pack(anchor="w", padx=20)
        # Focal 선택 옵션 (별개의 체크박스로 추가)
        ttk.Checkbutton(mpv_degree_frame, text=mpv_focal_option, variable=mpv_focal_var).pack(anchor="w", padx=20)
    else:
        mpv_degree_frame.pack_forget()  # Absent/Not provided 선택시 mpv_degree_frame을 숨김
        mpv_degree_var.set("")
        mpv_focal_var.set(False)

# MPV Contact 옵션 라디오버튼 패킹
mpv_rb = ttk.Radiobutton(mpv_contact_frame, text="Present", variable=mpv_var, value="Present", command=update_mpv_visibility)
mpv_rb.pack(anchor="w")

mpv2_rb = ttk.Radiobutton(mpv_contact_frame, text="Absent", variable=mpv_var, value="Absent", command=update_mpv_visibility)
mpv2_rb.pack(anchor="w")

mpv_not_provided_rb = ttk.Radiobutton(mpv_contact_frame, text="Not provided", variable=mpv_var, value="Not provided", command=update_mpv_visibility)
mpv_not_provided_rb.pack(anchor="w")

# SMV Contact 선택을 위한 Frame 생성 및 패킹
smv_contact_frame = tk.Frame(venous_frame)
smv_contact_frame.pack(fill="x")

smv_label = ttk.Label(smv_contact_frame, text="3-2. SMV Contact")
smv_label.pack(anchor="w", side=tk.TOP)

smv_var = tk.StringVar(value="Not provided")
smv_degree_var = tk.StringVar(value="")
smv_focal_var = tk.BooleanVar(value=False)

# Degree와 Focal 선택 옵션
smv_degree_options = ["≤ 180°", "> 180°"]
smv_focal_option = "Focal vessel narrowing or contour irregularity"

# Degree와 Focal 선택을 위한 Frame (초기엔 숨겨짐)
smv_degree_frame = tk.Frame(smv_contact_frame)

def update_smv_visibility():
    if smv_var.get() == "Present":
        smv_degree_frame.pack(fill="x", expand=True, after=smv_rb)  # Present 선택시 smv_degree_frame을 패킹
        for widget in smv_degree_frame.winfo_children():
            widget.destroy()  # 기존에 패킹된 위젯들을 제거
        for option in smv_degree_options:
            ttk.Radiobutton(smv_degree_frame, text=option, variable=smv_degree_var, value=option).pack(anchor="w", padx=20)
        # Focal 선택 옵션 (체크박스로 추가)
        ttk.Checkbutton(smv_degree_frame, text=smv_focal_option, variable=smv_focal_var).pack(anchor="w", padx=20)
    else:
        smv_degree_frame.pack_forget()  # Absent/Not provided 선택시 smv_degree_frame을 숨김
        smv_degree_var.set("")
        smv_focal_var.set(False)

# SMV Contact 옵션 라디오버튼 패킹
smv_rb = ttk.Radiobutton(smv_contact_frame, text="Present", variable=smv_var, value="Present", command=update_smv_visibility)
smv_rb.pack(anchor="w")

smv2_rb = ttk.Radiobutton(smv_contact_frame, text="Absent", variable=smv_var, value="Absent", command=update_smv_visibility)
smv2_rb.pack(anchor="w")

smv_not_provided_rb = ttk.Radiobutton(smv_contact_frame, text="Not provided", variable=smv_var, value="Not provided", command=update_smv_visibility)
smv_not_provided_rb.pack(anchor="w")


# Frame for the Extrapancreatic Evaluation section
extrapancreatic_frame = ttk.LabelFrame(right_column, text="4. Extrapancreatic Evaluation", style="Bold.TLabelframe")
extrapancreatic_frame.pack(fill="x", expand=False, padx=10, pady=5)

# Liver lesions subsection
liver_lesions_label = ttk.Label(extrapancreatic_frame, text="4-1. Liver lesions")
liver_lesions_label.pack(anchor="w")
liver_lesions_options = ["Present", "Suspicious", "Indeterminate", "Likely benign", "Absent", "Not provided"]
liver_lesions_var = tk.StringVar(value="Not provided")  # default value
for option in liver_lesions_options:
    ttk.Radiobutton(extrapancreatic_frame, text=option, variable=liver_lesions_var, value=option).pack(anchor="w")

# Peritoneal or omental nodules subsection
nodules_label = ttk.Label(extrapancreatic_frame, text="4-2. Peritoneal or omental nodules")
nodules_label.pack(anchor="w")
nodules_options = ["Present", "Absent", "Not provided"]
nodules_var = tk.StringVar(value="Not provided")  # default value
for option in nodules_options:
    ttk.Radiobutton(extrapancreatic_frame, text=option, variable=nodules_var, value=option).pack(anchor="w")

# Ascites subsection
ascites_label = ttk.Label(extrapancreatic_frame, text="4-3. Ascites")
ascites_label.pack(anchor="w")
ascites_options = ["Present", "Absent", "Not provided"]
ascites_var = tk.StringVar(value="Not provided")  # default value
for option in ascites_options:
    ttk.Radiobutton(extrapancreatic_frame, text=option, variable=ascites_var, value=option).pack(anchor="w")

# 4-4 Suspicious lymph nodes subsection
lymph_nodes_frame = ttk.LabelFrame(extrapancreatic_frame, text="4-4. Suspicious lymph nodes")
lymph_nodes_frame.pack(fill="x", expand="yes", padx=10, pady=5)

# Variable and function for lymph nodes
lymph_nodes_var = tk.StringVar(value="Not provided")
lymph_node_details = ["Porta hepatis", "Celiac", "Splenic hilum", "Paraaortic", "Aortocaval", "Other"]

# Create a frame to contain the checkboxes so they can be managed separately
checkbox_frame = tk.Frame(lymph_nodes_frame)

def handle_lymph_nodes_selection():
    # Remove the checkbox frame before rearranging
    checkbox_frame.pack_forget()
    if lymph_nodes_var.get() == "Present":
        # Show the Checkbuttons after the 'Present' radiobutton
        checkbox_frame.pack(after=present_rb, fill='x', expand=True)
        absent_rb.pack(after=checkbox_frame)
        not_provided_rb.pack(after=absent_rb)
    else:
        # Ensure that 'Absent' and 'Not provided' buttons are re-packed correctly
        absent_rb.pack(after=present_rb)
        not_provided_rb.pack(after=absent_rb)
        # Reset checkboxes
        for var in lymph_node_vars:
            var.set(False)

# Radio buttons for lymph node presence/absence
present_rb = ttk.Radiobutton(lymph_nodes_frame, text="Present", variable=lymph_nodes_var, value="Present",
                             command=handle_lymph_nodes_selection)
present_rb.pack(anchor="w")

absent_rb = ttk.Radiobutton(lymph_nodes_frame, text="Absent", variable=lymph_nodes_var, value="Absent",
                            command=handle_lymph_nodes_selection)
not_provided_rb = ttk.Radiobutton(lymph_nodes_frame, text="Not provided", variable=lymph_nodes_var, value="Not provided",
                                  command=handle_lymph_nodes_selection)

# Checkbuttons for lymph node details
lymph_node_vars = []
for detail in lymph_node_details:
    var = tk.BooleanVar()
    cb = ttk.Checkbutton(checkbox_frame, text=detail, variable=var)
    cb.pack(anchor="w", padx=20)
    lymph_node_vars.append(var)

# Pack the absent and not provided radio buttons in the correct order
absent_rb.pack(after=present_rb, anchor="w")
not_provided_rb.pack(after=absent_rb, anchor="w")


# 4-5 Other extrapancreatic disease subsection
other_disease_frame = ttk.LabelFrame(extrapancreatic_frame, text="4-5. Other extrapancreatic disease")
other_disease_frame.pack(fill="x", expand="yes", padx=10, pady=5)

# Text entry for organ involved, initially not visible
organ_involved_frame = tk.Frame(other_disease_frame)
organ_involved_label = ttk.Label(organ_involved_frame, text="Organ involved:")
organ_involved_entry = ttk.Entry(organ_involved_frame, width=50)

other_disease_var = tk.StringVar(value="Not provided")

def handle_other_disease_selection():
    if other_disease_var.get() == "Present":
        organ_involved_label.pack(side="left")
        organ_involved_entry.pack(side="left", fill="x", expand=True)
        organ_involved_frame.pack(fill="x", expand=True, after=present_other_rb)
    else:
        organ_involved_label.pack_forget()
        organ_involved_entry.pack_forget()
        organ_involved_frame.pack_forget()
        organ_involved_entry.delete(0, tk.END)

# Radio buttons for other extrapancreatic disease
present_other_rb = ttk.Radiobutton(other_disease_frame, text="Present", variable=other_disease_var, value="Present",
                         command=handle_other_disease_selection)
present_other_rb.pack(anchor="w")

absent_other_rb = ttk.Radiobutton(other_disease_frame, text="Absent", variable=other_disease_var, value="Absent",
                         command=handle_other_disease_selection)
absent_other_rb.pack(anchor="w")

not_provided_other_rb = ttk.Radiobutton(other_disease_frame, text="Not provided", variable=other_disease_var, value="Not provided",
                         command=handle_other_disease_selection)
not_provided_other_rb.pack(anchor="w")

# Frame for the Conclusion section
style = ttk.Style()
style.configure("Bold.TLabelframe.Label", font=('Arial', 14, 'bold'))
resectability_frame = ttk.LabelFrame(right_column, text="5. Conclusion", style="Bold.TLabelframe")
resectability_frame.pack(fill="x", expand=False, padx=10, pady=5)

# Resectability subsection
resect_label = ttk.Label(resectability_frame, text="5-1.Resectability")
resect_label.pack(anchor="w")
resect_options = ["Resectable", "Borderline Resectable", "Locally Advanced", "Metastatic disease", "Not Assessable"]
resect_var = tk.StringVar(value="Not Assessable")  # default value
for option in resect_options:
    ttk.Radiobutton(resectability_frame, text=option, variable=resect_var, value=option).pack(anchor="w")


# 메시지 출력을 위한 Label 위젯
status_label = ttk.Label(right_column, text="", font=('Arial', 14, 'bold'), foreground='red')
status_label.pack(pady=5)

# 버튼들을 담을 프레임 생성 및 배치
button_frame = tk.Frame(right_column)
button_frame.pack(pady=5)

# OK 버튼 추가 (기존 create_report 함수가 정의되어 있다고 가정)
ok_button = ttk.Button(button_frame, text="OK", command=create_report)
ok_button.pack(side=tk.LEFT, padx=(0, 10))  # OK 버튼을 왼쪽에 배치하고 오른쪽에 패딩 추가

# Next 버튼 추가 (기존 reset_radio_buttons 함수가 정의되어 있다고 가정)
next_button = ttk.Button(button_frame, text="Next", command=reset_radio_buttons)
next_button.pack(side=tk.LEFT)  # Next 버튼을 왼쪽에 배치 (OK 버튼 바로 옆)

# Start the main loop
root.mainloop()
