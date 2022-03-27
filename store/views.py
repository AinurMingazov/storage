from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .forms import OperationForm
from .models import Tool, Keeper, Operation, Category


def keeper_operations(request, keeper_slug=None):
    """Функция отображает все операции определенного владельца."""
    keepers = Keeper.objects.all()
    keeper = get_object_or_404(Keeper, slug=keeper_slug)
    operations = Operation.objects.filter(Q(taker=keeper) | Q(giver=keeper))
    return render(request,
                  'store/tool/operations.html',
                  {'keeper': keeper,
                   'keepers': keepers,
                   'operations': operations,
                   })


def tool_detail(request, id, slug):
    """Функция отображает подробную информацию о товаре."""
    tool = get_object_or_404(Tool,
                             id=id,
                             slug=slug,
                             available=True)

    return render(request,
                  'store/tool/detail.html',
                  {'tool': tool,
                   })


def tool_list(request, keeper_slug=None):
    """Функция показываем все инструменты по умолчанию,
    позволяет настроить фильтр по категориям и/или по владельцам."""
    category = Category.objects.all()
    keepers = Keeper.objects.all()
    tools = Tool.objects.filter(available=True, quantity__gt=0)
    selected_categories = request.GET.getlist('selected_categories')

    if selected_categories:
        keeper = get_object_or_404(Keeper, slug=keeper_slug)
        categories = Category.objects.filter(slug__in=selected_categories)
        tools = tools.filter(keeper=keeper, category__in=categories)
        return render(request,
                      'store/tool/list.html',
                      {'keeper': keeper,
                       'keepers': keepers,
                       'tools': tools,
                       'category': category,
                       'selected_categories': selected_categories,
                       'categories': categories
                       })
    else:

        if keeper_slug is not None:
            keeper = get_object_or_404(Keeper, slug=keeper_slug)
            tools = tools.filter(keeper=keeper)

            return render(request,
                          'store/tool/list.html',
                          {'keeper': keeper,
                           'keepers': keepers,
                           'tools': tools,
                           'category': category,
                           'query': selected_categories,
                           })
        else:
            return render(request,
                          'store/tool/list.html',
                          {'keepers': keepers,
                           'tools': tools,
                           'category': category,
                           'query': selected_categories,
                           })


def tool_operation(request, id, slug):
    """Функция отображает форму передачи инструмента.
    При получении POST запроса, проверяет наличие товара у получающего владельца,
    если есть добавляет в количество, если нет то создает."""

    tool = get_object_or_404(Tool, id=id)

    if request.method == "POST":
        form = OperationForm(request.POST)

        if form.is_valid():
            form_tool = Tool(name=tool.name, keeper=tool.keeper, slug=tool.slug, description=tool.description,
                             price=tool.price, quantity=tool.quantity, category=tool.category)
            form_tool.quantity = form.cleaned_data['quantity']
            form_tool.keeper = form.cleaned_data['keeper']
            # Проверка передачи инструмента более чем есть в наличии и передачи владельцом самому
            # себе. Передача не выполняется и возвращается страница формы.
            if tool.quantity < form_tool.quantity:
                form.add_error(None, "Недостаточно инструмента для передачи")
                return render(request,
                              'store/tool/operation.html',
                              {'tool': tool, 'form': form})
            if form_tool.keeper == tool.keeper:
                form.add_error(None, "Производится передача инструмента самому владельцу")
                return render(request,
                              'store/tool/operation.html',
                              {'tool': tool, 'form': form})

            tool.quantity = tool.quantity - form_tool.quantity

            try:
                t = Tool.objects.get(
                    name=form_tool.name,
                    keeper=form_tool.keeper,
                    category=tool.category)
                t.quantity += form_tool.quantity
                t.save()
                tool.save()

                operation = Operation.objects.create(
                    giver=tool.keeper, taker=form_tool.keeper,
                    tool=tool, quantity=form_tool.quantity)
                operation.save()
                return render(request,
                              'store/tool/detail.html',
                              {'tool': t,
                               })
            except ObjectDoesNotExist:
                tool.save()
                form_tool.save()
                operation = Operation.objects.create(
                    giver=tool.keeper, taker=form_tool.keeper,
                    tool=tool, quantity=form_tool.quantity)
                operation.save()
                return render(request,
                              'store/tool/detail.html',
                              {'tool': form_tool,
                               })

    else:
        form = OperationForm()

    return render(request,
                  'store/tool/operation.html',
                  {'tool': tool, 'form': form,
                   })
