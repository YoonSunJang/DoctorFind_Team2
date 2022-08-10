var option1 = document.querySelector('#option1');
var option2 = document.querySelector('#option2');
var option3 = document.querySelector('#option3');
var option4 = document.querySelector('#option4');
var option5 = document.querySelector('#option5');
var option6 = document.querySelector('#option6');

var check1 = false;
var check2 = false;
var check3 = false;
var check4 = false;
var check5 = false;
var check6 = false;

const CLICKED_CLASS="clicked"

function handleClick1(){
    if(check1==false){
        check1=true;
    }else{
        check1=false;
    }
    option1.classList.toggle(CLICKED_CLASS);
    console.log("진료중"+check1);
}
function handleClick2(){
    if(check2==false){
        check2=true;
    }else{
        check2=false;
    }
    option2.classList.toggle(CLICKED_CLASS);
    console.log("야간진료"+check2);
}
function handleClick3(){
    if(check3==false){
        check3=true;
    }else{
        check3=false;
    }
    option3.classList.toggle(CLICKED_CLASS);
    console.log("공휴일진료"+check3);
}
function handleClick4(){
    if(check4==false){
        check4=true;
    }else{
        check4=false;
    }
    option4.classList.toggle(CLICKED_CLASS);
    console.log("응급실주간"+check4);
}
function handleClick5(){
    if(check5==false){
        check5=true;
    }else{
        check5=false;
    }
    option5.classList.toggle(CLICKED_CLASS);
    console.log("응급실야간"+check5);
}
function handleClick6(){
    if(check6==false){
        check6=true;
    }else{
        check6=false;
    }
    option6.classList.toggle(CLICKED_CLASS);
    console.log("24시"+check6);
}

option1.addEventListener("click",handleClick1);
option2.addEventListener("click",handleClick2);
option3.addEventListener("click",handleClick3);
option4.addEventListener("click",handleClick4);
option5.addEventListener("click",handleClick5);
option6.addEventListener("click",handleClick6);

