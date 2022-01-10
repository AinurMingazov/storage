from django.shortcuts import render, get_object_or_404
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
    # cart_product_form = CartAddProductForm()
    return render(request,
                  'store/tool/detail.html',
                  {'tool': tool,
                   # 'cart_product_form': cart_product_form
                   })
