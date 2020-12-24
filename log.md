# Login #

GET https://ids.shanghaitech.edu.cn/authserver/login 


This will give you a form like this

```HTML
<form id="casLoginForm" role="form" 
    action="https://ids.shanghaitech.edu.cn/authserver/login" method="post">

    <input id="username" name="username" type="text" value="">
    <input id="password"  type="password" value="">
    <input id="passwordEncrypt" name="password" type="text" value="">

    <button type="button" class="auth_login_btn">Login
    
    <input type="hidden" name="lt" value="......">
    <input type="hidden" name="dllt" value="userNamePasswordLogin">
    <input type="hidden" name="execution" value="......">
    <input type="hidden" name="_eventId" value="submit">
    <input type="hidden" name="rmShown" value="......">
    <input type="hidden" id="pwdDefaultEncryptSalt" value="......">
</form>
```

with Javascript like this

```javascript
$(".auth_login_btn").click(function(){
    $("#casLoginForm").submit();
}

```

The password field in the form is real time encrypted.

The callee is in the function `_etd2(_p0, _p1)` in `login-wisedu_v1.0.js`. 

```javascript
    function _etd2(_p0, _p1) { 
        try { 
            var _p2 = encryptAES(_p0, _p1); 
            $("#casLoginForm").find("#passwordEncrypt").val(_p2); 
        } catch (e) { 
            $("#casLoginForm").find("#passwordEncrypt").val(_p0); 
        } 
    }
    var casLoginForm = $("#casLoginForm");
    var password = casLoginForm.find("#password");
    _etd2(password.val(), casLoginForm.find("#pwdDefaultEncryptSalt").val());
```
The encrpyt algorithm is AES, provided by CryptoJS,
using salt in the field `pwdDefaultEncryptSalt`, `casLoginForm`.

```javascript
let $_chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';
let _chars_len = $_chars.length;
function _rds(len) { 
    var retStr = ''; 
    for (i = 0; i < len; i++) 
        retStr += $_chars.charAt(Math.floor(Math.random() * _chars_len)); 
    return retStr; 
}

function _gas(data, key0, iv0) { 
        key0 = key0.replace(/(^\s+)|(\s+$)/g, ""); 
        var key = CryptoJS.enc.Utf8.parse(key0); 
        var iv = CryptoJS.enc.Utf8.parse(iv0); 
        var encrypted = CryptoJS.AES.encrypt(data, key, 
            {
                iv: iv, 
                mode: CryptoJS.mode.CBC, 
                padding: CryptoJS.pad.Pkcs7 
            }); 
        return encrypted.toString(); 
}

function encryptAES(data, _p1) { 
    if (!_p1) return data; 
    var encrypted = _gas(_rds(64) + data, _p1, _rds(16)); 
    return encrypted; 
}
```

All you need is to simulate a POST from a form.

Note:
1. When the encrpytion failed, the passwordEncrypt is literally the same as password. 
    
2. The `toString()` method is not simply convert the bytes to string, if you directly do this, you may get some errors. The fact is:

```javascript
var AES = require("crypto-js/aes");
var crypto = require("crypto-js");
a = AES.encrypt('123', '456')

// When you write this:
a.toString()
// crypto.js actually do this:
crypto.format.OpenSSL.stringify(a)

function stringify(cipherParams) {
    var wordArray;
    // Shortcuts
    var ciphertext = cipherParams.ciphertext;
    var salt = cipherParams.salt;

    // Format
    if (salt) {
        wordArray = WordArray.create([0x53616c74, 0x65645f5f]).
            concat(salt).concat(ciphertext);
    } else 
        wordArray = ciphertext;
    
    return wordArray.toString(Base64);
}
```


# Authentation #

When access https://eams.shanghaitech.edu.cn/eams/

The server will redirect to:

    https://ids.shanghaitech.edu.cn/authserver/
        login?service={url} 

The url is the service you want to access, for example:
    
    https://ids.shanghaitech.edu.cn/authserver/
        login?service=
            https%3A%2F%2Feams.shanghaitech.edu.cn%2Feams%2Flogin.action

After authentation server will distribute a JSESSIONID to the client side,

and redirect to the original web page. 
