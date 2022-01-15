from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .forms import OperationForm
from .models import Tool, Keeper, Operation


def tool_list(request, keeper_slug=None):
    keeper = None
    keepers = Keeper.objects.all()
    tools = Tool.objects.filter(available=True, quantity__gt=0)
    if keeper_slug:
        keeper = get_object_or_404(Keeper, slug=keeper_slug)
        tools = tools.filter(keeper=keeper)

    return render(request,
                  'store/tool/list.html',
                  {'keeper': keeper,
                   'keepers': keepers,
                   'tools': tools})


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
                             price=tool.price, quantity=tool.quantity)
            form_tool.quantity = form.cleaned_data['quantity']
            form_tool.keeper = form.cleaned_data['keeper']
            if tool.quantity < form_tool.quantity or form_tool.keeper == tool.keeper:
                # return HttpResponse("Invalid login details supplied.")
                # messages.error(request, 'Недостаточно инструмента.')
                return render(request,
                              'store/tool/operation.html',
                              {'tool': tool, 'form': form,'quantity':'Недостаточно инструмента.'
                               })

                # raise ValidationError("Недостаточно инструмента")
            tool.quantity = tool.quantity - form_tool.quantity

            try:
                t = Tool.objects.get(name=form_tool.name, keeper=form_tool.keeper)
                print(t.quantity)
                t.quantity += form_tool.quantity
                t.save()
                tool.save()
                return render(request,
                              'store/tool/detail.html',
                              {'tool': t,
                               })
            except ObjectDoesNotExist:
                tool.save()
                form_tool.save()
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
