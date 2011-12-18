function $(id){
    return document.getElementById(id);
}

function tell(s){
    x = $('result');
    x.value += s + '\n';
    x.scrollTop = x.scrollHeight;
}

function submit(totalSubmit,gotAc){
    if (gotAc==1){
        return;
    }
    if (totalSubmit >= 50){
        tell('Too BAD rp!!! Come back Later!');
        return;
    }
    async = true;
    info = '';
    info += 'username=' + $('username').value;
    info += "&"
    info += 'password=' + $('password').value;
    info += "&"
    info += 'totalSubmit=' + (totalSubmit + 1);
    req = new XMLHttpRequest();
    req.open('GET','/SubmitOnce?'+info,async);
    if (async){
        req.onreadystatechange = function(){
            if (req.readyState==4 && req.status==200){
                i = req.responseText;
                tell(i);
                if (i[0]=='Y'){
//                    tell('You\'ve got an AC!');
                    gotAc = 1;
                }
                else{
//                    tell('This is the ' + (totalSubmit+1) + ' time of submitting for you');
                }
                setTimeout('submit('+(totalSubmit+1)+','+gotAc+')',3000);
            }
        }
    }
    req.send();
}
