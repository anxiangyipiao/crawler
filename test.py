import re

code = """
<script>function a(a){function n(){for(var a={wQzOV:_0x649a("0x4"),iTyzs:function(a,n){return a+n}},n=a[_0x649a("0x5")][_0x649a("0x6")]("|"),e=0;;){switch(n[e++]){case"0":t+="EO_Bot_Ssid=";continue;case"1":return t;case"2":t+="";continue;case"3":t=a[_0x649a("0x7")](t,48758784);continue;case"4":var t="";continue}break}}var e={WTKkN:2717287998,bOYDu:480234661,dtzqS:function(a,n){return a+n},wyeCN:700406951,pCQRM:function(a){return a()}},t=0;return t+=e[_0x649a("0x0")],t+=e[_0x649a("0x1")],t=e[_0x649a("0x2")](t,e[_0x649a("0x3")]),[t,e[_0x649a("0x8")](n)][a]}var _0x49a6=["wyeCN","4|2|0|3|1","wQzOV","split","iTyzs","pCQRM","cookie","location.href=location.href.replace(/[?|&]tads/, '')","WTKkN","bOYDu","dtzqS"];(function(a,n){var e=function(n){for(;--n;)a.push(a.shift())};e(++n)})(_0x49a6,0x147);var _0x649a=function(a,n){a-=0;var e=_0x49a6[a];return e};document[_0x649a("0x9")]="__tst_status="+a(0)+"#;",document[_0x649a("0x9")]=a(1)+";",setTimeout(_0x649a("0xa"),0x4b0);</script>
"""

# 使用正则表达式匹配 case "3" 行中的数字
# re.DOTALL 让 . 可以匹配换行符
regex = r'case\s*"3":.*?\(t,\s*(\d+)\s*\);'
match = re.search(regex, code, re.DOTALL)

if match:
  extracted_number = match.group(1)
  print(extracted_number) # 输出: 48758784
else:
  print("未找到匹配的数字")



match_wtkkn = re.search(r"WTKkN\s*:\s*(\d+)", code).group(1)
        # 查找 bOYDu: 后面的数字
match_boydu = re.search(r"bOYDu\s*:\s*(\d+)", code).group(1)
        # 查找 wyeCN: 后面的数字
match_wyecn = re.search(r"wyeCN\s*:\s*(\d+)", code).group(1)

print(match_wtkkn)  # 输出: 2717287998

print(match_boydu)  # 输出: 480234661

print(match_wyecn)  # 输出: 700406951