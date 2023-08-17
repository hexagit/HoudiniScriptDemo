"""パラメーターJSONのセーブロードスクリプト

Houdiniの1SOPノードにあるすべてのパラメーターをJSONファイルに出力し、
そのJSONファイルを入力しSOPノードのすべてのパラメーターを上書きする機能を提供します。

Todo:
    * PythonSOPノードを追加（この例では"../python1"）し、Python Code欄にこのソースコードを貼り付ける
    * パラメーターのセーブロードを行いたいノードにEdit Parameter Interface...で次のインターフェースを追加する
    * Fileタイプのファイルパス入力欄を追加する（Nameは"FilePath"であること）
    * Buttonタイプの実行ボタンを追加し、Callback Script(Python)を次のようにする（セーブの場合）
    * exec(hou.node("../python1").parm("python").eval()); hx_save_parms()
"""


import json


def hx_get_parm(node_path, parm):
    """ノードのパラメーターの値を返す

    指定ノードの指定パラメーターの評価値を返します。

    Args:
        node_path (str): 指定ノードのパス
        parm (str): 指定パラメーター名

    Returns:
        指定パラメーターの評価値。

    """
    node = hou.node(node_path)
    return node.parm(parm).eval()


def hx_make_parms_dict(node_path):
    """ノードの全パラメーターを辞書化

    指定ノードの全パラメーターをdictにして返します。

    Args:
        node_path (str): 指定ノードのパス

    Returns:
        dict: パラメーター名と値の辞書。
        パラメーターがない場合は空辞書が返ります。

    """
    parms_dict = {}
    node = hou.node(node_path)
    for p in node.parms():
       parms_dict[p.name()] = p.eval()
    return parms_dict


def hx_save_parms():
    """JSONファイルにパラメーターをセーブ

    選択中のノードにある全パラメーターをJSON形式にして、
    FilePathパラメーターで指定したファイルパスのJSONファイルを出力します。
    
    Examples:
        exec(hou.node("../python1").parm("python").eval()); hx_save_parms()

    """
    node = hou.selectedNodes()[0]
    node_path = node.path()
    save_path = hx_get_parm(node_path, "FilePath")
    parms_dict = hx_make_parms_dict(node_path)
    with open(save_path, 'w') as f:
        json.dump(parms_dict, f, indent=2)


def hx_load_parms():
    """JSONファイルからパラメーターをロード

    FilePathパラメーターで指定したファイルパスのJSONファイルを入力し、
    選択中のノードにある同名のパラメーターに上書きします。

    Examples:
        exec(hou.node("../python1").parm("python").eval()); hx_load_parms()

    """
    node = hou.selectedNodes()[0]
    node_path = node.path()
    load_path = hx_get_parm(node_path, "FilePath")
    with open(load_path) as f:
        parms_dict = json.load(f)
    for k, v in parms_dict.items():
        try:
            node.parm(k).set(v)
        except hou.PermissionError:
            pass
