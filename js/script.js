const rollNumberUI = document.getElementById('roll_number');
const submitBtnUI = document.getElementById('submitbtn');


const ready = () => {
    rollNumberUI.focus();
}

const downloadPdf = (fileURL, fileName) => {
    let link = document.createElement('a');
    link.href = fileURL;
    link.download = fileName;
    link.dispatchEvent(new MouseEvent('click'));
}

const submitBtnHandler = () => {
    let rollNumber = rollNumberUI.value;
    downloadPdf(`../pdfs/${rollNumber}_marksheet.pdf`, rollNumber);
    rollNumberUI.value = '';
}

submitBtnUI.addEventListener('click', (e)=>{
    e.preventDefault();
    submitBtnHandler(); 
});
