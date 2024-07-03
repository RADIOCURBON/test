document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('cards-container');
    const cards = Array.from(container.getElementsByClassName('card'));

    // ���������� �������� �� �������� ��������
    cards.sort((a, b) => {
        const valueA = parseInt(a.querySelector('.name-too').innerText.replace(/\s/g, ''));
        const valueB = parseInt(b.querySelector('.name-too').innerText.replace(/\s/g, ''));
        return valueB - valueA;
    });

    // ������� ����������
    container.innerHTML = '';

    // ���������� ��������������� �������� ������� � ���������
    cards.forEach(card => container.appendChild(card));
});