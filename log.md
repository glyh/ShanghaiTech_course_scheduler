# Login #

GET https://ids.shanghaitech.edu.cn/authserver/login 


This will give you a form like this
```HTML
<form id="casLoginForm" class="fm-v clearfix amp-login-form" role="form" action="https://ids.shanghaitech.edu.cn/authserver/login" method="post">
    <input id="username" name="username" placeholder="用户名" class="auth_input" type="text" value="">
    <input id="password" placeholder="密码" class="auth_input" type="password" value="" autocomplete="off">
    <input id="passwordEncrypt" name="password" style="display:none;" type="text" value="">
    <button type="button" class="auth_login_btn primary full_width">登录
    <input type="hidden" name="lt" value="LT-159699-JhpPtWD3N1A00s9ZbS9EpdBHEtBsRn1608801124164-tmLB-cas">
    <input type="hidden" name="dllt" value="userNamePasswordLogin">
    <input type="hidden" name="execution" value="e2s1">
    <input type="hidden" name="_eventId" value="submit">
    <input type="hidden" name="rmShown" value="1">
    <input type="hidden" id="pwdDefaultEncryptSalt" value="pvX1aEVbmcdqoHZp">
</form>
```

The password field in the form is real time encrypted.

The callee is in the function `_etd(_p0)` in `login-wisedu_v1.0.js`. 

The encrpyt algorithm is AES, provided by CryptoJS,
using salt in the field `pwdDefaultEncryptSalt`, `casLoginForm`.

When the encrpytion failed, the passwordEncrypt is literally the same as password. 

To make clear how the algorithm really works, is now beyond my ability, so I just 
write down this log to keep an record. 

# Authentation #
GET https://ids.shanghaitech.edu.cn/authserver/login?service={url} 