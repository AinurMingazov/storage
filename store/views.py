from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .forms import OperationForm
from .models import Tool, Keeper, Operation, Category


def keeper_operations(request, keeper_slug=None):
    keepers = Keeper.objects.all()
    keeper = get_object_or_404(Keeper, slug=keeper_slug)
    operations = Operation.objects.filter(Q(taker=keeper) | Q(giver=keeper))
    return render(request,
                  'store/tool/operations.html',
                  {'keeper': keeper,
                   'keepers': keepers,
                   'operations': operations,
                   })


def tool_list(request, keeper_slug='centralnyj-sklad'):

    category = Category.objects.all()
    keepers = Keeper.objects.all()
    tools = Tool.objects.filter(available=True, quantity__gt=0)
    q = request.GET.getlist('q')

    if q:
        keeper = get_object_or_404(Keeper, slug=keeper_slug)
        categories = Category.objects.filter(slug__in=q)
        tools = tools.filter(keeper=keeper, category__in=categories)

    else:
        keeper = get_object_or_404(Keeper, slug=keeper_slug)
        tools = tools.filter(keeper=keeper)

    return render(request,
                  'store/tool/list.html',
                  {'keeper': keeper,
                   'keepers': keepers,
                   'tools': tools,
                   'category': category,
                   'query': q,
                   })


def tool_detail(request, id, slug):
    tool = get_object_or_404(Tool,
                             id=id,
                             slug=slug,
                             available=True)

    return render(request,
                  'store/tool/detail.html',
                  {'tool': tool,
                   })


def tool_operation(request, id, slug):
    tool = get_object_or_404(Tool, id=id)

    if request.method == "POST":
        form = OperationForm(request.POST)

        if form.is_valid():
            form_tool = Tool(name=tool.name, keeper=tool.keeper, slug=tool.slug, description=tool.description,
                             price=tool.price, quantity=tool.quantity, category=tool.category)
            form_tool.quantity = form.cleaned_data['quantity']
            form_tool.keeper = form.cleaned_data['keeper']
            if tool.quantity < form_tool.quantity or form_tool.keeper == tool.keeper:
                # return HttpResponse("Invalid login details supplied.")
                # messages.error(request, 'Недостаточно инструмента.')
                return render(request,
                              'store/tool/operation.html',
                              {'tool': tool, 'form': form, 'quantity': 'Недостаточно инструмента.'
                               })

                # raise ValidationError("Недостаточно инструмента")
            tool.quantity = tool.quantity - form_tool.quantity

            try:
                t = Tool.objects.get(name=form_tool.name, keeper=form_tool.keeper, category=tool.category)
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
