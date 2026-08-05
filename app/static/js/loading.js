const uploadForm = document.getElementById("uploadForm");
const overlay = document.getElementById("loadingOverlay");
const timer = document.getElementById("timer");
const progressBar = document.getElementById("progressBar");
const steps = [
	"step1",
	"step2",
	"step3",
	"step4",
	"step5",
	"step6",
	"step7",
	"step8",
	"step9",
	"step10",
	"step11"
];
if(uploadForm){
	uploadForm.addEventListener("submit",function(){
		overlay.style.display="flex";
		let seconds=0;
		timer.innerHTML="&#x23F1;&#xFE0F; 00:00";
		setInterval(function(){
			seconds++;
		        let m=Math.floor(seconds/60);
		        let s=seconds%60;
			timer.innerHTML = 
			"&#x23F1;&#xFE0F; " + 
			String(m).padStart(2, "0") + 
			":" + 
			String(s).padStart(2, "0");
		},1000);
		let progress=0;
		steps.forEach((id,index)=>{
			setTimeout(()=>{
				let item=document.getElementById(id);
				item.classList.remove("waiting");
				item.classList.add("completed");
				item.innerHTML = "&#x2705; " + item.innerHTML.substring(2);
				progress=((index+1)/steps.length)*100;
				progressBar.style.width=progress+"%";
				progressBar.innerHTML=Math.round(progress)+"%";
			},(index+1)*1500);
		});
	});
}
