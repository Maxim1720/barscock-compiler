const btn = document.querySelector(".btn")
let api_url = `/api`

btn.addEventListener('click', (e) => {
    const input = document.querySelector('.code-input');
    fetch(`${api_url}/analyze`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "data": input.value
        })
    })
        .then(r => r.json()) // Получаем JSON из ответа
        .then(data => {
            console.log(data); // Логируем данные

            // res = (Object.values(data).map(i=>i.join(' '))).join("<br>")
            res = Object.keys(data).map(k=> k + ": " + data[k].join(" ")).join("<br/>")

            // console.log(res)
            document.querySelector('.lex-analyze').innerHTML = res
            //"tw: " + data.tw.join(' ') + "<br>" + "tl: " + data.tl.join(' ') + "<br>" + "tn: " + data.tn.join(' ') + "<br>"; // Выводим данные
        })
        .catch(err => {
            document.querySelector('.lex-analyze').innerHTML = err;
        });

});
