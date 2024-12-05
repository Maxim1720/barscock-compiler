const btn = document.querySelector(".btn");
let api_url = `/api`;
syntaxResultSelector = document.querySelector('.syntax_result')
semanticResultSelector = document.querySelector('.semantic_result')

btn.addEventListener('click', () => {
    const input = document.querySelector('.code-input');
    fetch(`${api_url}/lexical`, {
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

            console.log(data)

            // Получаем тело таблицы
            const tableBody = document.querySelector('.lex-analyze');
            tableBody.innerHTML = ""; // Очищаем таблицу перед заполнением

            // Находим максимальное количество строк (для выравнивания)
            const maxRows = Math.max(
                data.tw?.length || 0,
                data.ti?.length || 0,
                data.tl?.length || 0,
                data.tn?.length || 0
            );

            // Генерируем строки таблицы
            for (let i = 0; i < maxRows; i++) {
                const row = document.createElement('tr');

                // Функция для создания ячейки с данными
                const createCell = (array, index) => {
                    const cell = document.createElement('td');
                    cell.textContent = array && array[index] ? array[index] : "—";
                    return cell;
                };

                // Добавляем ячейки в строку
                row.appendChild(createCell(data.tw, i)); // Ключевые слова
                row.appendChild(createCell(data.ti, i)); // Идентификаторы
                row.appendChild(createCell(data.tl, i)); // Разделители
                row.appendChild(createCell(data.tn, i)); // Числа

                // Добавляем строку в таблицу
                tableBody.appendChild(row);
            }
            if(data.state === "ERROR"){
                throw Error("Ошибка при анализе")
            }
        })
        .catch(err => {
            console.error("Ошибка запроса:", err);

            syntaxResultSelector.innerHTML = ""
            semanticResultSelector.innerHTML = ""

            const tableBody = document.querySelector('.lex-analyze');
            tableBody.innerHTML = `
                <tr>
                    <td colspan="4" class="text-danger">Произошла ошибка: ${err.message}</td>
                </tr>`;
        });



    fetch(`${api_url}/syntax`, {
        method: 'POST',
        headers: {
            "Accept": "application/json"
        }
    })
        .then(r => {
            if (r.ok) {
                syntaxResultSelector.innerHTML = "Синтаксический анализ прошел успешно"
                syntaxResultSelector.classList.add("bg-success")
                syntaxResultSelector.classList.remove("bg-danger")

                semanticResultSelector.innerHTML = "Семантический анализ прошел успешно"
                semanticResultSelector.classList.add("bg-success")
                semanticResultSelector.classList.remove("bg-danger")
            } else {
                r.json().then(
                    data => {
                        selector = data.error === 'type' ? semanticResultSelector : syntaxResultSelector
                        selector.innerHTML = data.message
                        selector.classList.add("bg-danger")
                        selector.classList.remove("bg-success")

                        selectors = [
                            syntaxResultSelector, semanticResultSelector
                        ]

                        selectors.forEach(
                            s=>{
                                if (s !== selector){
                                    s.innerHTML = ""
                                    s.classList.remove("bg-success")
                                    s.classList.remove("bg-danger")
                                }
                            }
                        )

                    }
                )
            }
        })
        .catch(err => {
            alert(err)
            // syntaxResultSelector.innerHTML = err.message
            // syntaxResultSelector.classList.add('bg-danger')
            // syntaxResultSelector.classList.remove('bg-success')
        })

});
