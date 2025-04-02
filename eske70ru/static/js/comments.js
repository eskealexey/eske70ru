document.addEventListener('DOMContentLoaded', function() {
    // Обработка кнопки "Ответить"
    document.querySelectorAll('.reply-btn').forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.getAttribute('data-comment-id');
            const replyForm = this.nextElementSibling;

            // Скрыть все другие открытые формы
            document.querySelectorAll('.reply-form').forEach(form => {
                if (form !== replyForm) {
                    form.style.display = 'none';
                }
            });

            // Показать/скрыть текущую форму
            if (replyForm.style.display === 'none') {
                replyForm.style.display = 'block';
            } else {
                replyForm.style.display = 'none';
            }
        });
    });

    // Обработка кнопки "Отмена"
    document.querySelectorAll('.cancel-reply').forEach(button => {
        button.addEventListener('click', function() {
            this.closest('.reply-form').style.display = 'none';
        });
    });
});
