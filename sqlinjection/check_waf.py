from core import is_similar_page


def check_have_waf(old_html,new_html):
    if not old_html or not new_html:
        return True
    if is_similar_page(old_html,new_html,radio=0.4):
        #有防火墙返回true，页面相似度小于6
        return True
    else:
        return False

#测试数据
