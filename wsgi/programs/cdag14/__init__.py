import cherrypy

# 這是 CDAG14 類別的定義
class CDAG14(object):
    # 各組利用 index 引導隨後的程式執行
    @cherrypy.expose
    def index(self, *args, **kwargs):
        outstring = '''
這是 2014CDA 協同專案下的 cdag14 分組程式開發網頁, 以下為 W12 的任務執行內容.<br />
<!-- 這裡採用相對連結, 而非網址的絕對連結 (這一段為 html 註解) -->
<a href="cube1">cdag14 正方體參數繪圖</a>(尺寸變數 a, b, c)<br /><br />
<a href="fourbar1">四連桿組立</a><br /><br />
<a href="assembly">remsub6</a><br /><br />
<a href="assembly1">remsub</a><br /><br />
<a href="assembly3">remsub44444</a><br /><br />
請確定下列連桿位於 V:/home/fourbar 目錄中, 且開啟空白 Creo 組立檔案.<br />
<a href="/static/fourbar.7z">fourbar.7z</a>(滑鼠右鍵存成 .7z 檔案)<br />
'''
        return outstring


# 這是 REMSUB6 類別的定義




    @cherrypy.expose
    def assembly3(self, *args, **kwargs):
        outstring =         '''
        <!DOCTYPE html> 
        <html>
        <head>
        <meta http-equiv="content-type" content="text/html;charset=utf-8">
        <script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
        </head>
        <body>
        </script><script language="JavaScript">
/*設計一個零件組立函示
get 組立
get part
抓取約束元素 in part and asm
選擇約束型式
應用在 part 上
*/
/*
軸面接
axis_plane_assembly(session, assembly, transf, featID, constrain_way, part2, axis1, plane1, axis2, plane2)
====================
assembly 組立檔案
transf 座標矩陣
feadID 要組裝的父
part2 要組裝的子
 
constrain_way 參數
1 對齊 對齊
2 對齊 貼合
else 按照 1
 
plane1~plane2 要組裝的父 參考面
plane3~plane4 要組裝的子 參考面
*/
function axis_plane_assembly(file_location, session, assembly, transf, featID, constrain_way, axis1, plane1, axis2, plane2) {
    //設定part2 路徑
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName(file_location);
    //嘗試從 session 中取得 part2
    var componentModel = session.GetModelFromDescr(descr);
    //取得失敗 status null
    if (componentModel == null) {
        document.write("在session 取得不到零件" + file_location);
        //從路逕取得 part2
        componentModel = session.RetrieveModel(descr);
        //仍然取得失敗 表示無此零件
        if (componentModel == null) {
            // 此發錯誤
            throw new Error(0, "Current componentModel is not loaded.");
        }
    }
    //假如 part2 有取得到
    if (componentModel != void null) {
        //將part2 放入 組立檔案, part2 在組立檔案裡面為 組立 component
        var asmcomp = assembly.AssembleComponent(componentModel, transf);
    }
 
    //組立父 featID list 形態, 為整數型態 list
    var ids = pfcCreate("intseq");
    //當有提供 要組裝的父
    if (featID != -1) {
        //將要組裝的父 加入 list
        ids.Append(featID);
        //取得組裝路徑
        //建立路徑變數，CreateComponentPath:回傳組件的路徑物件，把組立模型和的ID路徑給所需的組件。
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        var subassembly = subPath.Leaf;
    } else {
        // 假如沒有提供 要組裝的父
        // asm 基本 就當作父零件
        var subassembly = assembly;
        //取得組裝路徑
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    }
 
    //父參考 element
    var asmDatums = new Array(axis1, plane1);
    //子參考 element
    var compDatums = new Array(axis2, plane2);
 
    //約數型態
    if (constrain_way == 1) {
        var relation = new Array(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
    } else if (constrain_way == 2) {
        var relation = new Array(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
    } else {
        var relation = new Array(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
 
    }
 
    //選擇元素 形態 (ITEM_AXIS) 軸 (ITEM_SURFACE) 面
    var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE);
    //約束 list 等下要應用於 子
    var constrs = pfcCreate("pfcComponentConstraints");
 
    for (var i = 0; i < 2; i++) {
        //選擇 父元素
        var asmItem = subassembly.GetItemByName(relationItem[i], asmDatums[i]);
        if (asmItem == void null) {
            interactFlag = true;
            continue;
        }
        //選擇 子元素
        var compItem = componentModel.GetItemByName(relationItem[i], compDatums[i]);
        if (compItem == void null) {
            interactFlag = true;
            continue;
        }
 
        //採用互動式設定相關的變數
        var MpfcSelect = pfcCreate("MpfcSelect");
        //互動式設定 選擇元素 父
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        //互動式設定 選擇元素 子
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        //選擇約束形態
        var constr = pfcCreate("pfcComponentConstraint").Create(relation[i]);
        //約束選擇 剛剛得父元素
        constr.AssemblyReference = asmSel;
        //約束選擇 剛剛得子元素
        constr.ComponentReference = compSel;
        //設定約束屬性
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create(true, false);
        //加入此約束 至 約束 list
        constrs.Append(constr);
    }
    //約束 list應用至 子
    asmcomp.SetConstraints(constrs, void null);
    //回傳 component id
    return asmcomp.Id;
}
// 以上為 axis_plane_assembly() 函式
/*
三面接
three_plane_assembly(session, assembly, transf, featID, constrain_way, part2, plane1, plane2, plane3, plane4, plane5, plane6)
=====================
assembly 組立檔案
transf 座標矩陣
feadID 要組裝的父
part2 要組裝的子
 
constrain_way 參數
1 對齊
2 貼合
else 按照 1
 
plane1~plane3 要組裝的父 參考面
plane4~plane6 要組裝的子 參考面
*/
function three_plane_assembly(file_location, session, assembly, transf, featID, constrain_way, plane1, plane2, plane3, plane4, plane5, plane6) {
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName(file_location);
    var componentModel = session.GetModelFromDescr(descr);
    if (componentModel == null) {
        document.write("在session 取得不到零件" + file_location);
        componentModel = session.RetrieveModel(descr);
        if (componentModel == null) {
            throw new Error(0, "Current componentModel is not loaded.");
        }
    }
    if (componentModel != void null) {
        var asmcomp = assembly.AssembleComponent(componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    //假如  asm 有零件時候
    if (featID != -1) {
 
        ids.Append(featID);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        var subassembly = subPath.Leaf;
    }
    // 假如是第一個零件 asm 就當作父零件
    else {
        var subassembly = assembly;
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    }
 
 
    var constrs = pfcCreate("pfcComponentConstraints");
    var asmDatums = new Array(plane1, plane2, plane3);
    var compDatums = new Array(plane4, plane5, plane6);
    var MpfcSelect = pfcCreate("MpfcSelect");
    for (var i = 0; i < 3; i++) {
        var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
 
        if (asmItem == void null) {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
        if (compItem == void null) {
            interactFlag = true;
            continue;
        }
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        if (constrain_way == 1) {
            var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
        } else if (constrain_way == 2) {
            var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
        } else {
            var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
        }
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create(false, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    return asmcomp.Id;
}
// 以上為 three_plane_assembly() 函式
 
 
//1軸2面
function one_axis_two_plane_assembly(file_location, session, assembly, transf, featID, constrain_way, axis1, plane1_1, plane1_2, axis2, plane2_1, plane2_2) {
    //設定part2 路徑
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName(file_location);
    //嘗試從 session 中取得 part2
    var componentModel = session.GetModelFromDescr(descr);
    //取得失敗 status null
    if (componentModel == null) {
        document.write("在session 取得不到零件" + file_location);
        //從路逕取得 part2
        componentModel = session.RetrieveModel(descr);
        //仍然取得失敗 表示無此零件
        if (componentModel == null) {
            // 此發錯誤
            throw new Error(0, "Current componentModel is not loaded.");
        }
    }
    //假如 part2 有取得到
    if (componentModel != void null) {
        //將part2 放入 組立檔案, part2 在組立檔案裡面為 組立 component
        var asmcomp = assembly.AssembleComponent(componentModel, transf);
    }
 
    //組立父 featID list 形態, 為整數型態 list
    var ids = pfcCreate("intseq");
    //當有提供 要組裝的父
    if (featID != -1) {
        //將要組裝的父 加入 list
        ids.Append(featID);
        //取得組裝路徑
        //建立路徑變數，CreateComponentPath:回傳組件的路徑物件，把組立模型和的ID路徑給所需的組件。
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        var subassembly = subPath.Leaf;
    } else {
        // 假如沒有提供 要組裝的父
        // asm 基本 就當作父零件
        var subassembly = assembly;
        //取得組裝路徑
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    }
 
    //父參考 element
    var asmDatums = new Array(axis1, plane1_1, plane1_2);
    //子參考 element
    var compDatums = new Array(axis2, plane2_1, plane2_2);
 
    //約數型態
    var ConstraintType = pfcCreate("pfcComponentConstraintType");
    if (constrain_way == 1) {
        var relation = new Array(ConstraintType.ASM_CONSTRAINT_ALIGN, ConstraintType.ASM_CONSTRAINT_MATE, ConstraintType.ASM_CONSTRAINT_AUTO);
    } else if (constrain_way == 2) {
        var relation = new Array(ConstraintType.ASM_CONSTRAINT_ALIGN, ConstraintType.ASM_CONSTRAINT_ALIGN, ConstraintType.ASM_CONSTRAINT_MATE);
    } else if (constrain_way == 3) {
        var relation = new Array(ConstraintType.ASM_CONSTRAINT_ALIGN, ConstraintType.ASM_CONSTRAINT_MATE, ConstraintType.ASM_CONSTRAINT_MATE);
    } else {
        var relation = new Array(ConstraintType.ASM_CONSTRAINT_ALIGN, ConstraintType.ASM_CONSTRAINT_ALIGN, ConstraintType.ASM_CONSTRAINT_ALIGN);
 
    }
 
    //選擇元素 形態 (ITEM_AXIS) 軸 (ITEM_SURFACE) 面
    var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE, pfcCreate("pfcModelItemType").ITEM_SURFACE);
    //約束 list 等下要應用於 子
    var constrs = pfcCreate("pfcComponentConstraints");
 
    for (var i = 0; i < 3; i++) {
        //選擇 父元素
        var asmItem = subassembly.GetItemByName(relationItem[i], asmDatums[i]);
        if (asmItem == void null) {
            interactFlag = true;
            continue;
        }
        //選擇 子元素
        var compItem = componentModel.GetItemByName(relationItem[i], compDatums[i]);
        if (compItem == void null) {
            interactFlag = true;
            continue;
        }
 
        //採用互動式設定相關的變數
        var MpfcSelect = pfcCreate("MpfcSelect");
        //互動式設定 選擇元素 父
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        //互動式設定 選擇元素 子
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        //選擇約束形態
        var constr = pfcCreate("pfcComponentConstraint").Create(relation[i]);
        //約束選擇 剛剛得父元素
        constr.AssemblyReference = asmSel;
        //約束選擇 剛剛得子元素
        constr.ComponentReference = compSel;
        //設定約束屬性
        //constr.Attributes = pfcCreate("pfcConstraintAttributes").Create(true, false);
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create(true, false);
        //加入此約束 至 約束 list
        constrs.Append(constr);
    }
    //約束 list應用至 子
    asmcomp.SetConstraints(constrs, void null);
    //回傳 component id
    return asmcomp.Id;
}
 
 
//
// 假如 Creo 所在的操作系統不是 Windows 環境
if (!pfcIsWindows()) {
    // 則啟動對應的 UniversalXPConnect 執行權限 (等同 Windows 下的 ActiveX)
    netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
}
// pfcGetProESession() 是位於 pfcUtils.js 中的函式, 確定此 JavaScript 是在嵌入式瀏覽器中執行
var session = pfcGetProESession();
// 設定 config option, 不要使用元件組立流程中內建的假設約束條件
session.SetConfigOption("comp_placement_assumptions", "no");
// 建立擺放零件的位置矩陣, Pro/Web.Link 中的變數無法直接建立, 必須透過 pfcCreate() 建立
var identityMatrix = pfcCreate("pfcMatrix3D");
// 建立 identity 位置矩陣
for (var x = 0; x < 4; x++) {
    for (var y = 0; y < 4; y++) {
        if (x == y) {
            identityMatrix.Set(x, y, 1.0);
        } else {
            identityMatrix.Set(x, y, 0.0);
        }
    }
}
// 利用 identityMatrix 建立 transf 座標轉換矩陣
var transf = pfcCreate("pfcTransform3D").Create(identityMatrix);
// 取得目前的工作目錄
var currentDir = session.getCurrentDirectory();
// 以目前已開檔的空白組立檔案, 作為 model
var model = session.CurrentModel;
// 查驗有無 model, 或 model 類別是否為組立件, 若不符合條件則丟出錯誤訊息
if (model == void null || model.Type != pfcCreate("pfcModelType").MDL_ASSEMBLY)
    throw new Error(0, "Current model is not an assembly.");
// 將此模型設為組立物件
var assembly = model;
 
/*
three_plane_assembly(session, assembly, transf, featID, constrain_way, part2, plane1, plane2, plane3, plane4, plane5, plane6)
=====================
assembly 組立檔案
transf 座標矩陣
feadID 要組裝的父
part2 要組裝的子
 
constrain_way 參數
1 對齊
2 貼合
else 按照 1
 
plane1~plane3 要組裝的父 參考面
plane4~plane6 要組裝的子 參考面
 
axis_plane_assembly(session, assembly, transf, featID, constrain_way, part2, axis1, plane1, axis2, plane2)
====================
assembly 組立檔案
transf 座標矩陣
feadID 要組裝的父
part2 要組裝的子
 
constrain_way 參數
1 對齊 對齊
2 對齊 貼合
else 按照 1
 
plane1~plane2 要組裝的父 參考面
plane3~plane4 要組裝的子 參考面
*/






 
var work_directory = "V:/home/lego/remsub/"
//function three_plane_assembly(file_location, session, assembly, transf, featID, constrain_way, plane1, plane2, plane3, plane4, plane5, plane6) {

var body_id = three_plane_assembly(work_directory + "crossblockb.prt", session, assembly, transf, -1, 1, "ASM_FRONT", "ASM_TOP", "ASM_RIGHT", "FRONT", "TOP", "RIGHT");

//function one_axis_two_plane_assembly(file_location, session, assembly, transf, featID, constrain_way, axis1, plane1_1, plane1_2, axis2, plane2_1, plane2_2)

var beam_7 = one_axis_two_plane_assembly(work_directory +"beam_7.prt", session, assembly, transf, body_id, 1, "RIGHT", "A_25", "DTM4", "DTM1", "A_42", "TOP");
 
var crossblockb = one_axis_two_plane_assembly(work_directory + "crossblockb", session, assembly, transf, body_id, 1, "RIGHT", "FRONT", "DTM2", "DTM1", "FRONT", "DTM5");

/* 
//var crossblock_2_left = one_axis_two_plane_assembly(work_directory + 'crossblock_2.prt', session, assembly, transf, body_id, 1, "A_25", "DTM3","FRONT",  "A_16", "DTM4", "DTM1");
 
//var crossblock_2_right = one_axis_two_plane_assembly(work_directory + 'crossblock_2.prt', session, assembly, transf, body_id, 1, "A_25", "DTM1","FRONT",  "A_16", "DTM5", "DTM1");
 
//var crossblock_2_left_front = one_axis_two_plane_assembly(work_directory + 'crossblock_2.prt', session, assembly, transf, body_id, 2, "A_26", "DTM4", "DTM1",  "A_16", "DTM1", "DTM4");
 
//var crossblock_2_right_front = one_axis_two_plane_assembly(work_directory + 'crossblock_2.prt', session, assembly, transf, body_id, 2, "A_26", "DTM4", "DTM3",  "A_16", "DTM1", "DTM5");
 
//var crossblock_2_left_2 = one_axis_two_plane_assembly(work_directory + 'crossblock_2.prt', session, assembly, transf, crossblock_2_left, 2, "A_16", "DTM2", "DTM5",  "A_16", "DTM1", "DTM4");
 
//var crossblock_2_right_2 = one_axis_two_plane_assembly(work_directory + 'crossblock_2.prt', session, assembly, transf, crossblock_2_right, 2, "A_16", "DTM2", "DTM4",  "A_16", "DTM1", "DTM5");
 
//var conn_3_left = axis_plane_assembly(work_directory + 'conn_3.prt', session, assembly, transf, crossblock_2_left, 1, "A_17", "DTM10", "A_20", "DTM1");
 
//var conn_3_left = axis_plane_assembly(work_directory + 'conn_3.prt', session, assembly, transf, crossblock_2_right, 1, "A_17", "DTM10", "A_20", "DTM1");
 
//var beam_3 = one_axis_two_plane_assembly(work_directory + 'beam_3.prt', session, assembly, transf, crossblock_2_right, 3,
    "A_17", "DTM7","FRONT",  "A_37", "BOTTOM", "RIGHT");
 */
assembly.Regenerate(void null);
session.GetModelWindow(assembly).Repaint();
</script>
</body>
</html>
'''
        return outstring




    @cherrypy.expose
    def assembly1(self, *args, **kwargs):
        outstring = '''
<!DOCTYPE html> 
<html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
</head>
<body>
</script><script language="JavaScript">
/*remsub6.py 完全利用函式呼叫進行組立*/
/*設計一個零件組立函式*/
// featID 為組立件第一個組立零件的編號
// inc 則為 part1 的組立順序編號, 第一個入組立檔編號為 featID+0
// part2 為外加的零件名稱
////////////////////////////////////////////////
// axis_plane_assembly 組立函式
////////////////////////////////////////////////
function axis_plane_assembly(session, assembly, transf, featID, inc, part2, axis1, plane1, axis2, plane2){
var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/remsub/"+part2);
var componentModel = session.GetModelFromDescr(descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
    var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
var ids = pfcCreate("intseq");
ids.Append(featID+inc);
var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
subassembly = subPath.Leaf;
var asmDatums = new Array(axis1, plane1);
var compDatums = new Array(axis2, plane2);
var relation = new Array (pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE);
var constrs = pfcCreate("pfcComponentConstraints");
    for (var i = 0; i < 2; i++)
    {
        var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var MpfcSelect = pfcCreate ("MpfcSelect");
        var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create (relation[i]);
        constr.AssemblyReference  = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (true, false);
        constrs.Append(constr);
    }
asmcomp.SetConstraints(constrs, void null);
}
// 以上為 axis_plane_assembly() 函式
///////////////////////////////////////////////////////////////////////////////////////////////////////////
// three_plane_assembly 採 align 組立, 若 featID 為 0 表示為空組立檔案
///////////////////////////////////////////////////////////////////////////////////////////////////////////
function three_plane_assembly(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/remsub/"+part2);
var componentModel = session.GetModelFromDescr(descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
    var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
var ids = pfcCreate("intseq");
// 若 featID 為 0 表示為空組立檔案
if (featID != 0){
    ids.Append(featID+inc);
    var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    subassembly = subPath.Leaf;
    }else{
    var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    subassembly = assembly;
    // 設法取得第一個組立零件 first_featID
    // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
    var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
    // 此一 featID 為組立件中的第一個零件編號
    var first_featID = components.Item(0).Id;
    }
var constrs = pfcCreate("pfcComponentConstraints");
var asmDatums = new Array(plane1, plane2, plane3);
var compDatums = new Array(plane4, plane5, plane6);
var MpfcSelect = pfcCreate("MpfcSelect");
for (var i = 0; i < 3; i++)
{
    var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
    
    if (asmItem == void null)
    {
        interactFlag = true;
        continue;
    }
    var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
    if (compItem == void null)
    {
        interactFlag = true;
        continue;
    }
    var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
    var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
    var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
    constr.AssemblyReference = asmSel;
    constr.ComponentReference = compSel;
    constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
    constrs.Append(constr);
}
asmcomp.SetConstraints(constrs, void null);
// 若 featID = 0 則傳回 first_featID
if (featID == 0)
    return first_featID;
}
// 以上為 three_plane_assembly() 函式
///////////////////////////////////////////////////////////////////////////////////////////////////////////
// three_plane_assembly2 採 mate 組立, 若 featID 為 0 表示為空組立檔案
///////////////////////////////////////////////////////////////////////////////////////////////////////////
function three_plane_assembly2(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/remsub/"+part2);
var componentModel = session.GetModelFromDescr(descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
    var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
var ids = pfcCreate("intseq");
// 若 featID 為 0 表示為空組立檔案
if (featID != 0){
    ids.Append(featID+inc);
    var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    subassembly = subPath.Leaf;
    }else{
    var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    subassembly = assembly;
    // 設法取得第一個組立零件 first_featID
    // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
    var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
    // 此一 featID 為組立件中的第一個零件編號
    var first_featID = components.Item(0).Id;
    }
var constrs = pfcCreate("pfcComponentConstraints");
var asmDatums = new Array(plane1, plane2, plane3);
var compDatums = new Array(plane4, plane5, plane6);
var MpfcSelect = pfcCreate("MpfcSelect");
for (var i = 0; i < 3; i++)
{
    var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
    
    if (asmItem == void null)
    {
        interactFlag = true;
        continue;
    }
    var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
    if (compItem == void null)
    {
        interactFlag = true;
        continue;
    }
    var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
    var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
    var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
    constr.AssemblyReference = asmSel;
    constr.ComponentReference = compSel;
    constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
    constrs.Append(constr);
}
asmcomp.SetConstraints(constrs, void null);
// 若 featID = 0 則傳回 first_featID
if (featID == 0)
    return first_featID;
}
// 以上為 three_plane_assembly2() 函式, 主要採三面 MATE 組立
//
// 假如 Creo 所在的操作系統不是 Windows 環境
if (!pfcIsWindows())
// 則啟動對應的 UniversalXPConnect 執行權限 (等同 Windows 下的 ActiveX)
netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
// pfcGetProESession() 是位於 pfcUtils.js 中的函式, 確定此 JavaScript 是在嵌入式瀏覽器中執行
var session = pfcGetProESession();
// 設定 config option, 不要使用元件組立流程中內建的假設約束條件
session.SetConfigOption("comp_placement_assumptions","no");
// 建立擺放零件的位置矩陣, Pro/Web.Link 中的變數無法直接建立, 必須透過 pfcCreate() 建立
var identityMatrix = pfcCreate("pfcMatrix3D");
// 建立 identity 位置矩陣
for (var x = 0; x < 4; x++)
for (var y = 0; y < 4; y++)
{
    if (x == y)
        identityMatrix.Set(x, y, 1.0);
    else
        identityMatrix.Set(x, y, 0.0);
}
// 利用 identityMatrix 建立 transf 座標轉換矩陣
var transf = pfcCreate("pfcTransform3D").Create(identityMatrix);
// 取得目前的工作目錄
var currentDir = session.getCurrentDirectory();
// 以目前已開檔的空白組立檔案, 作為 model
var model = session.CurrentModel;
// 查驗有無 model, 或 model 類別是否為組立件, 若不符合條件則丟出錯誤訊息
if (model == void null || model.Type != pfcCreate("pfcModelType").MDL_ASSEMBLY)
throw new Error (0, "Current model is not an assembly.");
// 將此模型設為組立物件
var assembly = model;

/////////////////////////////////////////////////////////////////
// 開始執行組立, 全部採函式呼叫組立
/////////////////////////////////////////////////////////////////

// Body 與空組立檔案採三個平面約束組立
// 空組立面為 ASM_TOP, ASM_FRONT, ASM_RIGHT
// Body 組立面為 TOP, FRONT, RIGHT
// 若 featID=0 表示為空組立檔案, 而且函式會傳回第一個組立件的 featID

var featID = three_plane_assembly(session, assembly, transf, 0, 0, "crossblockb.prt", "ASM_TOP", "ASM_FRONT", "ASM_RIGHT", "TOP", "FRONT", "RIGHT"); 

//var featID = three_plane_assembly(session, assembly, transf, 0, 0, "beam_7.prt", "ASM_TOP", "ASM_FRONT", "ASM_RIGHT", "TOP", "FRONT", "RIGHT"); 

alert("第一個零件特徵 ID 為:"+featID);

// BEAM_ANGLE.prt 中間面為 middle_green, 其餘定位面則為 red 與 blue
// AXLE_10.prt 中間面為 DTM1, Right 與 Front 則為定位面
// featID, 0 表示為 BEAM_ANGLE.prt 零件, "middle_green", "red", "blue" 為其定位面
// AXLE_10.prt 的定位面則為 "DTM1"(green), "RIGHT"(red), "FRONT"(blue)


//1
three_plane_assembly(session, assembly, transf, featID, 0, "axle_5.prt", "DTM5", "A_1", "DTM1", "RIGHT", "A_4", "DTM1");

//2
//three_plane_assembly(session, assembly, transf, featID, 0, "axle_5.prt", "DTM4", "FRONT", "DTM7", "RIGHT", "FRONT", "TOP");

//3
//three_plane_assembly(session, assembly, transf, featID, 0, "beam_7.prt", "RIGHT", "A_25", "DTM4", "DTM1", "A_42", "TOP");

//4
//three_plane_assembly(session, assembly, transf, featID, 1, "crossblockb.prt", "RIGHT", "FRONT", "DTM2", "DTM1", "FRONT", "DTM5");
 



//5
//three_plane_assembly(session, assembly, transf, featID, 0, "crossblockb.prt", "F6", "A_36", "A_38", "F9", "A_4", "A_3");

//6
//three_plane_assembly(session, assembly, transf, featID, 0, "crossblockb.prt", "F6", "A_36", "A_38", "F9", "A_4", "A_3");

//7
//three_plane_assembly(session, assembly, transf, featID, 0, "crossblockb.prt", "F6", "A_36", "A_38", "F9", "A_4", "A_3");

 



//alert("AXLE_10.prt 已經定位完成!");

// regenerate 並且 repaint 組立檔案
assembly.Regenerate (void null);
session.GetModelWindow (assembly).Repaint();    
</script>
</body>
</html>
'''
        return outstring












# 這是 REMSUB6 類別的定義

    @cherrypy.expose
    def assembly(self, *args, **kwargs):
        outstring = '''
<!DOCTYPE html> 
<html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
</head>
<body>
</script><script language="JavaScript">
/*remsub6.py 完全利用函式呼叫進行組立*/
/*設計一個零件組立函式*/
// featID 為組立件第一個組立零件的編號
// inc 則為 part1 的組立順序編號, 第一個入組立檔編號為 featID+0
// part2 為外加的零件名稱
////////////////////////////////////////////////
// axis_plane_assembly 組立函式
////////////////////////////////////////////////
function axis_plane_assembly(session, assembly, transf, featID, inc, part2, axis1, plane1, axis2, plane2){
var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/remsub6/"+part2);
var componentModel = session.GetModelFromDescr(descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
    var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
var ids = pfcCreate("intseq");
ids.Append(featID+inc);
var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
subassembly = subPath.Leaf;
var asmDatums = new Array(axis1, plane1);
var compDatums = new Array(axis2, plane2);
var relation = new Array (pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE);
var constrs = pfcCreate("pfcComponentConstraints");
    for (var i = 0; i < 2; i++)
    {
        var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var MpfcSelect = pfcCreate ("MpfcSelect");
        var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create (relation[i]);
        constr.AssemblyReference  = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (true, false);
        constrs.Append(constr);
    }
asmcomp.SetConstraints(constrs, void null);
}
// 以上為 axis_plane_assembly() 函式
///////////////////////////////////////////////////////////////////////////////////////////////////////////
// three_plane_assembly 採 align 組立, 若 featID 為 0 表示為空組立檔案
///////////////////////////////////////////////////////////////////////////////////////////////////////////
function three_plane_assembly(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/remsub6/"+part2);
var componentModel = session.GetModelFromDescr(descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
    var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
var ids = pfcCreate("intseq");
// 若 featID 為 0 表示為空組立檔案
if (featID != 0){
    ids.Append(featID+inc);
    var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    subassembly = subPath.Leaf;
    }else{
    var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    subassembly = assembly;
    // 設法取得第一個組立零件 first_featID
    // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
    var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
    // 此一 featID 為組立件中的第一個零件編號
    var first_featID = components.Item(0).Id;
    }
var constrs = pfcCreate("pfcComponentConstraints");
var asmDatums = new Array(plane1, plane2, plane3);
var compDatums = new Array(plane4, plane5, plane6);
var MpfcSelect = pfcCreate("MpfcSelect");
for (var i = 0; i < 3; i++)
{
    var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
    
    if (asmItem == void null)
    {
        interactFlag = true;
        continue;
    }
    var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
    if (compItem == void null)
    {
        interactFlag = true;
        continue;
    }
    var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
    var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
    var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
    constr.AssemblyReference = asmSel;
    constr.ComponentReference = compSel;
    constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
    constrs.Append(constr);
}
asmcomp.SetConstraints(constrs, void null);
// 若 featID = 0 則傳回 first_featID
if (featID == 0)
    return first_featID;
}
// 以上為 three_plane_assembly() 函式
///////////////////////////////////////////////////////////////////////////////////////////////////////////
// three_plane_assembly2 採 mate 組立, 若 featID 為 0 表示為空組立檔案
///////////////////////////////////////////////////////////////////////////////////////////////////////////
function three_plane_assembly2(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/remsub6/"+part2);
var componentModel = session.GetModelFromDescr(descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
    var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
var ids = pfcCreate("intseq");
// 若 featID 為 0 表示為空組立檔案
if (featID != 0){
    ids.Append(featID+inc);
    var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    subassembly = subPath.Leaf;
    }else{
    var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    subassembly = assembly;
    // 設法取得第一個組立零件 first_featID
    // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
    var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
    // 此一 featID 為組立件中的第一個零件編號
    var first_featID = components.Item(0).Id;
    }
var constrs = pfcCreate("pfcComponentConstraints");
var asmDatums = new Array(plane1, plane2, plane3);
var compDatums = new Array(plane4, plane5, plane6);
var MpfcSelect = pfcCreate("MpfcSelect");
for (var i = 0; i < 3; i++)
{
    var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
    
    if (asmItem == void null)
    {
        interactFlag = true;
        continue;
    }
    var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
    if (compItem == void null)
    {
        interactFlag = true;
        continue;
    }
    var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
    var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
    var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
    constr.AssemblyReference = asmSel;
    constr.ComponentReference = compSel;
    constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
    constrs.Append(constr);
}
asmcomp.SetConstraints(constrs, void null);
// 若 featID = 0 則傳回 first_featID
if (featID == 0)
    return first_featID;
}
// 以上為 three_plane_assembly2() 函式, 主要採三面 MATE 組立
//
// 假如 Creo 所在的操作系統不是 Windows 環境
if (!pfcIsWindows())
// 則啟動對應的 UniversalXPConnect 執行權限 (等同 Windows 下的 ActiveX)
netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
// pfcGetProESession() 是位於 pfcUtils.js 中的函式, 確定此 JavaScript 是在嵌入式瀏覽器中執行
var session = pfcGetProESession();
// 設定 config option, 不要使用元件組立流程中內建的假設約束條件
session.SetConfigOption("comp_placement_assumptions","no");
// 建立擺放零件的位置矩陣, Pro/Web.Link 中的變數無法直接建立, 必須透過 pfcCreate() 建立
var identityMatrix = pfcCreate("pfcMatrix3D");
// 建立 identity 位置矩陣
for (var x = 0; x < 4; x++)
for (var y = 0; y < 4; y++)
{
    if (x == y)
        identityMatrix.Set(x, y, 1.0);
    else
        identityMatrix.Set(x, y, 0.0);
}
// 利用 identityMatrix 建立 transf 座標轉換矩陣
var transf = pfcCreate("pfcTransform3D").Create(identityMatrix);
// 取得目前的工作目錄
var currentDir = session.getCurrentDirectory();
// 以目前已開檔的空白組立檔案, 作為 model
var model = session.CurrentModel;
// 查驗有無 model, 或 model 類別是否為組立件, 若不符合條件則丟出錯誤訊息
if (model == void null || model.Type != pfcCreate("pfcModelType").MDL_ASSEMBLY)
throw new Error (0, "Current model is not an assembly.");
// 將此模型設為組立物件
var assembly = model;

/////////////////////////////////////////////////////////////////
// 開始執行組立, 全部採函式呼叫組立
/////////////////////////////////////////////////////////////////

// Body 與空組立檔案採三個平面約束組立
// 空組立面為 ASM_TOP, ASM_FRONT, ASM_RIGHT
// Body 組立面為 TOP, FRONT, RIGHT
// 若 featID=0 表示為空組立檔案, 而且函式會傳回第一個組立件的 featID

var featID = three_plane_assembly(session, assembly, transf, 0, 0, "BEAM_ANGLE.prt", "ASM_TOP", "ASM_FRONT", "ASM_RIGHT", "TOP", "FRONT", "RIGHT"); 

alert("第一個零件特徵 ID 為:"+featID);

// BEAM_ANGLE.prt 中間面為 middle_green, 其餘定位面則為 red 與 blue
// AXLE_10.prt 中間面為 DTM1, Right 與 Front 則為定位面
// featID, 0 表示為 BEAM_ANGLE.prt 零件, "middle_green", "red", "blue" 為其定位面
// AXLE_10.prt 的定位面則為 "DTM1"(green), "RIGHT"(red), "FRONT"(blue)

three_plane_assembly(session, assembly, transf, featID, 0, "AXLE_10.prt", "middle_green", "red", "blue", "DTM1", "RIGHT", "FRONT");

alert("AXLE_10.prt 已經定位完成!");

// regenerate 並且 repaint 組立檔案
assembly.Regenerate (void null);
session.GetModelWindow (assembly).Repaint();    
</script>
</body>
</html>
'''
        return outstring








    ''' 
    假如採用下列規畫
    
    import programs.cdag14 as cdag14
    root.cdag14 = cdag14.CDAG14()
    
    則程式啟動後, 可以利用 /cdag14/cube1 呼叫函式執行
    '''
    @cherrypy.expose
    def cube1(self, *args, **kwargs):
        '''
    // 假如要自行打開特定零件檔案
    // 若第三輸入為 false, 表示僅載入 session, 但是不顯示
    // ret 為 model open return
    var ret = document.pwl.pwlMdlOpen("axle_5.prt", "v:/tmp", false);
    if (!ret.Status) {
        alert("pwlMdlOpen failed (" + ret.ErrorCode + ")");
    }
    //將 ProE 執行階段設為變數 session
    var session = pfcGetProESession();
    // 在視窗中打開零件檔案, 並且顯示出來
    var window = session.OpenFile(pfcCreate("pfcModelDescriptor").CreateFromFileName("axle_5.prt"));
    var solid = session.GetModel("axle_5.prt",pfcCreate("pfcModelType").MDL_PART);
        '''
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcParameterExamples.js"></script>
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcComponentFeatExamples.js"></script>
    </head>
    <body>
    <script type="text/javascript">
var session = pfcGetProESession ();

// 以目前所開啟的檔案為 solid model
// for volume
var solid = session.CurrentModel;

var a, b, c, i, j, aValue, bValue, cValue, volume, count;
// 將模型檔中的 a 變數設為 javascript 中的 a 變數
a = solid.GetParam("a");
b = solid.GetParam("b");
c = solid.GetParam("c");
volume=0;
count=0;
try
{
    for(i=0;i<5;i++)
    {
        myf = 100;
        myn = myf + i*10;
        // 設定變數值, 利用 ModelItem 中的 CreateDoubleParamValue 轉換成 Pro/Web.Link 所需要的浮點數值
    aValue = pfcCreate ("MpfcModelItem").CreateDoubleParamValue(myn);
    bValue = pfcCreate ("MpfcModelItem").CreateDoubleParamValue(myn);
    // 將處理好的變數值, 指定給對應的零件變數
    a.Value = aValue;
    b.Value = bValue;
    //零件尺寸重新設定後, 呼叫 Regenerate 更新模型
    solid.Regenerate(void null);
    //利用 GetMassProperty 取得模型的質量相關物件
    properties = solid.GetMassProperty(void null);
    volume = properties.Volume;
    count = count + 1;
    alert("執行第"+count+"次,零件總體積:"+volume);
    // 將零件存為新檔案
    //var newfile = document.pwl.pwlMdlSaveAs("filename.prt", "v:/tmp", "filename_5_"+count+".prt");
    // 測試  stl 轉檔
    //var stl_csys = "PRT_CSYS_DEF";
    //var stl_instrs = new pfcCreate ("pfcSTLASCIIExportInstructions").Create(stl_csys);
    //stl_instrs.SetQuality(10);  
    //solid.Export("v:/tmp/filename_5_"+count+".stl", stl_instrs); 
    // 結束測試轉檔
    //if (!newfile.Status) {
            //alert("pwlMdlSaveAs failed (" + newfile.ErrorCode + ")");
        //}
    } // for loop
}
catch (err)
{
    alert ("Exception occurred: "+pfcGetExceptionType (err));
}
    </script>
    </body>
    </html>
    '''
        return outstring
        
    @cherrypy.expose
    def fourbar1(self, *args, **kwargs):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
    </head>
    <body>
<script type="text/javascript">
if (!pfcIsWindows())
netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
var session = pfcGetProESession();
// 設定 config option
session.SetConfigOption("comp_placement_assumptions","no");
// 建立擺放零件的位置矩陣
var identityMatrix = pfcCreate ("pfcMatrix3D");
for (var x = 0; x < 4; x++)
	for (var y = 0; y < 4; y++)
	{
		if (x == y)
			identityMatrix.Set (x, y, 1.0);
		else
			identityMatrix.Set (x, y, 0.0);
	}
var transf = pfcCreate ("pfcTransform3D").Create (identityMatrix);
// 取得目前的工作目錄
var currentDir = session.getCurrentDirectory();
// 以目前已開檔, 作為 model
var model = session.CurrentModel;
// 查驗有無 model, 或 model 類別是否為組立件
if (model == void null || model.Type != pfcCreate ("pfcModelType").MDL_ASSEMBLY)
throw new Error (0, "Current model is not an assembly.");
var assembly = model;

/**----------------------------------------------- link0 -------------------------------------------------------------**/
    //檔案目錄，建議將圖檔放置工作目錄下較方便使用
	var descr = pfcCreate ("pfcModelDescriptor").CreateFromFileName ("v:/home/fourbar/link0.prt");
	// 若 link1.prt 在 session 則直接取用
	var componentModel = session.GetModelFromDescr (descr);
	//若 link1.prt 不在 session 則從工作目錄中載入 session
	var componentModel = session.RetrieveModel(descr);
	//若 link1.prt 已經在 session 則放入組立檔中
	if (componentModel != void null)
	{
		//注意這個 asmcomp 即為設定約束條件的本體
		//asmcomp 為特徵物件,直接將零件, 以 transf 座標轉換放入組立檔案中
		var asmcomp = assembly.AssembleComponent (componentModel, transf);
	}

// 建立約束條件變數
var constrs = pfcCreate ("pfcComponentConstraints");
//設定組立檔中的三個定位面, 注意內定名稱與 Pro/E WF 中的 ASM_D_FRONT 不同, 而是 ASM_FRONT
var asmDatums = new Array ("ASM_FRONT", "ASM_TOP", "ASM_RIGHT");
//設定零件檔中的三個定位面, 名稱與 Pro/E WF 中相同
var compDatums = new Array ("FRONT", "TOP", "RIGHT");
	//建立 ids 變數, intseq 為 sequence of integers 為資料類別, 使用者可以經由整數索引擷取此資料類別的元件, 第一個索引為 0
	var ids = pfcCreate ("intseq");
	//建立路徑變數
	var path = pfcCreate ("MpfcAssembly").CreateComponentPath (assembly, ids);
	//採用互動式設定相關的變數
	var MpfcSelect = pfcCreate ("MpfcSelect");
//利用迴圈分別約束組立與零件檔中的三個定位平面
for (var i = 0; i < 3; i++)
{
	//設定組立參考面
	var asmItem = assembly.GetItemByName (pfcCreate ("pfcModelItemType").ITEM_SURFACE, asmDatums [i]);
	//若無對應的組立參考面, 則啟用互動式平面選擇表單 flag
	if (asmItem == void null)
	{
		interactFlag = true;
		continue;
	}
	//設定零件參考面
	var compItem = componentModel.GetItemByName (pfcCreate ("pfcModelItemType").ITEM_SURFACE, compDatums [i]);
	//若無對應的零件參考面, 則啟用互動式平面選擇表單 flag
	if (compItem == void null)
	{
		interactFlag = true;
		continue;
	}
	var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, path);
	var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
	var constr = pfcCreate ("pfcComponentConstraint").Create (pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
	constr.AssemblyReference = asmSel;
	constr.ComponentReference = compSel;
	constr.Attributes = pfcCreate ("pfcConstraintAttributes").Create (false, false);
	//將互動選擇相關資料, 附加在程式約束變數之後
	constrs.Append (constr);
}

//設定組立約束條件
asmcomp.SetConstraints (constrs, void null);
/**-------------------------------------------------------------------------------------------------------------------**/

/**----------------------------------------------- link1 -------------------------------------------------------------**/
var descr = pfcCreate ("pfcModelDescriptor").CreateFromFileName ("v:/home/fourbar/link1.prt");
var componentModel = session.GetModelFromDescr (descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
	var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
var featID = components.Item(0).Id;

ids.Append(featID);
var subPath = pfcCreate ("MpfcAssembly").CreateComponentPath( assembly, ids );
subassembly = subPath.Leaf;
var asmDatums = new Array ("A_1", "TOP", "ASM_TOP");
var compDatums = new Array ("A_1", "TOP", "TOP");
var relation = new Array (pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS,pfcCreate("pfcModelItemType").ITEM_SURFACE);
var constrs = pfcCreate ("pfcComponentConstraints");
for (var i = 0; i < 2; i++)
	{
		var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
		if (asmItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
		if (compItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var MpfcSelect = pfcCreate ("MpfcSelect");
		var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
		var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
		var constr = pfcCreate ("pfcComponentConstraint").Create (relation[i]);
		constr.AssemblyReference  = asmSel;
		constr.ComponentReference = compSel;
		constr.Attributes = pfcCreate ("pfcConstraintAttributes").Create (true, false);
		constrs.Append (constr);
	}
asmcomp.SetConstraints (constrs, void null);

	
/**-------------------------------------------------------------------------------------------------------------------**/

/**----------------------------------------------- link2 -------------------------------------------------------------**/
var descr = pfcCreate ("pfcModelDescriptor").CreateFromFileName ("v:/home/fourbar/link2.prt");
var componentModel = session.GetModelFromDescr (descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
	var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
var ids = pfcCreate ("intseq");
ids.Append(featID+1);
var subPath = pfcCreate ("MpfcAssembly").CreateComponentPath( assembly, ids );
subassembly = subPath.Leaf;
var asmDatums = new Array ("A_2", "TOP", "ASM_TOP");
var compDatums = new Array ("A_1", "TOP", "TOP");
var relation = new Array (pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS,pfcCreate("pfcModelItemType").ITEM_SURFACE);
var constrs = pfcCreate ("pfcComponentConstraints");
for (var i = 0; i < 2; i++)
	{
		var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
		if (asmItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
		if (compItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var MpfcSelect = pfcCreate ("MpfcSelect");
		var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
		var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
		var constr = pfcCreate ("pfcComponentConstraint").Create (relation[i]);
		constr.AssemblyReference  = asmSel;
		constr.ComponentReference = compSel;
		constr.Attributes = pfcCreate ("pfcConstraintAttributes").Create (true, false);
		constrs.Append (constr);
	}
asmcomp.SetConstraints (constrs, void null);

	
/**-------------------------------------------------------------------------------------------------------------------**/


/**----------------------------------------------- link3 -------------------------------------------------------------**/
var descr = pfcCreate ("pfcModelDescriptor").CreateFromFileName ("v:/home/fourbar/link3.prt");
var componentModel = session.GetModelFromDescr (descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
	var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
var relation = new Array (pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS,pfcCreate("pfcModelItemType").ITEM_SURFACE);
var constrs = pfcCreate ("pfcComponentConstraints");

var ids = pfcCreate ("intseq");
ids.Append(featID+2);
var subPath = pfcCreate ("MpfcAssembly").CreateComponentPath( assembly, ids );
subassembly = subPath.Leaf;
var asmDatums = new Array ("A_2");
var compDatums = new Array ("A_1");
for (var i = 0; i < 1; i++)
	{
		var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
		if (asmItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
		if (compItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var MpfcSelect = pfcCreate ("MpfcSelect");
		var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
		var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
		var constr = pfcCreate ("pfcComponentConstraint").Create (relation[i]);
		constr.AssemblyReference  = asmSel;
		constr.ComponentReference = compSel;
		constr.Attributes = pfcCreate ("pfcConstraintAttributes").Create (true, false);
		constrs.Append (constr);
	}
asmcomp.SetConstraints (constrs, void null);


var ids = pfcCreate ("intseq");

ids.Append(featID);
var subPath = pfcCreate ("MpfcAssembly").CreateComponentPath( assembly, ids );
subassembly = subPath.Leaf;
var asmDatums = new Array ("A_2", "TOP");
var compDatums = new Array ("A_2", "BOTTON");
for (var i = 0; i < 2; i++)
	{
		var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
		if (asmItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
		if (compItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var MpfcSelect = pfcCreate ("MpfcSelect");
		var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
		var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
		var constr = pfcCreate ("pfcComponentConstraint").Create (relation[i]);
		constr.AssemblyReference  = asmSel;
		constr.ComponentReference = compSel;
		constr.Attributes = pfcCreate ("pfcConstraintAttributes").Create (true, true);
		constrs.Append (constr);
	}
asmcomp.SetConstraints (constrs, void null);

/**-------------------------------------------------------------------------------------------------------------------**/

var session = pfcGetProESession ();
var solid = session.CurrentModel;

properties = solid.GetMassProperty(void null);
var COG = properties.GravityCenter;
document.write("MassProperty:<br />");
document.write("Mass:"+(properties.Mass.toFixed(2))+"       pound<br />");
document.write("Average Density:"+(properties.Density.toFixed(2))+"       pound/inch^3<br />");
document.write("Surface area:"+(properties.SurfaceArea.toFixed(2))+"           inch^2<br />");
document.write("Volume:"+(properties.Volume.toFixed(2))+"   inch^3<br />");
document.write("COG_X:"+COG.Item(0).toFixed(2)+"<br />");
document.write("COG_Y:"+COG.Item(1).toFixed(2)+"<br />");
document.write("COG_Z:"+COG.Item(2).toFixed(2)+"<br />");

try
{
document.write("Current Directory:<br />"+currentDir);
}
catch (err)
{
alert ("Exception occurred: "+pfcGetExceptionType (err));
}
assembly.Regenerate (void null);
session.GetModelWindow (assembly).Repaint();
</script>
    </body>
    </html>
    '''
        return outstring

