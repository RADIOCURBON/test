document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('cards-container');
    const cards = Array.from(container.getElementsByClassName('card'));

    // —ортировка карточек по убыванию значений
    cards.sort((a, b) => {
        const valueA = parseInt(a.querySelector('.name-too').innerText.replace(/\s/g, ''));
        const valueB = parseInt(b.querySelector('.name-too').innerText.replace(/\s/g, ''));
        return valueB - valueA;
    });

    // ќчистка контейнера
    container.innerHTML = '';

    // ƒобавление отсортированных карточек обратно в контейнер
    cards.forEach(card => container.appendChild(card));
});