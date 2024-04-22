from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

"""
#前端html
<div class="container">
    <div class="row justify-content-center">
        <div class="col-auto">
            <nav aria-label="Page navigation">
                <ul class="pagination">
                    <li class="page-item">
                        <a class="page-link" href="?key={{ key }}&page=1">首页</a>
                    </li>
                    {% if page_obj.number > 1 %}
                        <li class="page-item">
                            <a class="page-link"
                               href="?key={{ key }}&page={{ page_obj.previous_page_number }}">&laquo;
                                上一页</a>
                        </li>
                    {% else %}
                        <li class="page-item">
                            <a class="page-link"
                               href="?key={{ key }}&page=1">&laquo;
                                上一页</a>
                        </li>
                    {% endif %}

                    {% for num in page_obj.paginator.page_range %}
                        {% if page_obj.number == num %}
                            <li class="page-item active"><a class="page-link"
                                                            href="?key={{ key }}&page={{ num }}">{{ num }}</a>
                            </li>
                        {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                            <li class="page-item"><a class="page-link"
                                                     href="?key={{ key }}&page={{ num }}">{{ num }}</a>
                            </li>
                        {% endif %}
                    {% endfor %}

                    {% if page_obj.has_next %}
                        <li class="page-item">
                            <a class="page-link"
                               href="?key={{ key }}&page={{ page_obj.next_page_number }}">下一页
                                &raquo;</a>
                        </li>
                        {% else %}
                        <li class="page-item">
                            <a class="page-link"
                               href="?key={{ key }}&page={{ page_obj.number }}">下一页
                                &raquo;</a>
                        </li>
                    {% endif %}
                    <li class="page-item">
                        <a class="page-link"
                           href="?key={{ key }}&page={{ page_obj.paginator.num_pages }}">尾页</a>
                    </li>
                </ul>
            </nav>
        </div>

        <div class="col-auto">
            <form class="form-inline">
                <div class="form-group">
                    <label for="page-number">跳转到页码:</label>
                    <input type="number" class="form-control mx-2" id="page-number"
                           min="1" max="{{ page_obj.paginator.num_pages }}"
                           value="{{ page_obj.number }}">
                    <button type="submit" class="btn btn-primary"
                            onclick="event.preventDefault(); window.location.href='?key={{ key }}&page=' + document.getElementById('page-number').value;">
                        跳转
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>


#后端

elders = Elder.objects.filter(is_active=True)
page_obj = Pagination(request, elders)
context = {
"page_obj": page_obj,
}

"""


def Pagination(request, object, items_per_page=6):
    """
    :param request: 请求头
    :param object: 数据库对象
    :param items_per_page: 页面展示数量
    :return: 页面对象
    """
    # 创建Paginator对象
    paginator = Paginator(object, items_per_page)
    # 从GET请求中获取页码，默认为1
    page_number = request.GET.get('page', 1)
    try:
        # 尝试获取请求页码的页面对象
        page_obj = paginator.page(page_number)
        return page_obj
    except PageNotAnInteger:
        # 如果页码不是整数，展示第一页
        page_obj = paginator.page(1)
        return page_obj
    except EmptyPage:
        # 如果页码超出范围，展示最后一页
        page_obj = paginator.page(paginator.num_pages)
        return page_obj
