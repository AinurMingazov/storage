from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import LoginUserForm, OperationForm, RegisterUserForm
from .models import Category, Keeper, Operation, Tool


class KeeperOperations(LoginRequiredMixin, ListView):
    """Класс описывает операции владельца инструментов"""

    paginate_by = 20
    model = Operation
    template_name = "store/tool/operations.html"
    context_object_name = "operations"
    slug_url_kwarg = "keeper_slug"

    def get_context_data(self, keeper_slug=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["keepers"] = Keeper.objects.all()
        context["keeper"] = Keeper.objects.filter(slug=self.kwargs["keeper_slug"])[0]
        return context

    def get_queryset(self):
        return Operation.objects.filter(
            Q(taker__slug=self.kwargs["keeper_slug"]) | Q(giver__slug=self.kwargs["keeper_slug"])
        ).select_related("giver", "taker", "tool")


class ToolDetail(DetailView):
    """Класс описывает инструмент"""

    model = Tool
    template_name = "store/tool/detail.html"
    context_object_name = "tool"
    pk_url_kwarg = "pk"

    def get_queryset(self):
        return Tool.objects.filter(pk=self.kwargs["pk"]).select_related("keeper")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        context["keepers"] = Keeper.objects.all()
        return context


class ToollList(ListView):
    """Класс описывает список инструментов"""

    paginate_by = 3
    model = Tool
    template_name = "store/tool/list.html"
    context_object_name = "tools"
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        context["keepers"] = Keeper.objects.all()
        context["keeper"] = self.keeper
        return context

    def get_queryset(self):
        return Tool.objects.filter(
            keeper=self.keeper,
            quantity__gt=0,
            available=True,
        )


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "store/tool/register.html"
    success_url = reverse_lazy("store:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("store:tool_list")


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "store/tool/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy("store:tool_list")


def logout_user(request):
    logout(request)
    return redirect("store:login")


def tool_list(request, keeper_slug=None):
    """Функция показываем все инструменты по умолчанию,
    позволяет настроить фильтр по категориям и/или по владельцам."""
    category = Category.objects.all()
    keepers = Keeper.objects.all()
    tools = Tool.objects.filter(available=True, quantity__gt=0)
    selected_categories = request.GET.getlist("selected_categories")

    if selected_categories:
        keeper = get_object_or_404(Keeper, slug=keeper_slug)
        categories = Category.objects.filter(slug__in=selected_categories)
        tools = tools.filter(keeper=keeper, category__in=categories)
        return render(
            request,
            "store/tool/list.html",
            {
                "keeper": keeper,
                "keepers": keepers,
                "tools": tools,
                "category": category,
                "selected_categories": selected_categories,
                "categories": categories,
            },
        )
    else:
        if keeper_slug is not None:
            keeper = get_object_or_404(Keeper, slug=keeper_slug)
            tools = tools.filter(keeper=keeper)

            return render(
                request,
                "store/tool/list.html",
                {
                    "keeper": keeper,
                    "keepers": keepers,
                    "tools": tools,
                    "category": category,
                    "query": selected_categories,
                },
            )
        else:
            return render(
                request,
                "store/tool/list.html",
                {
                    "keepers": keepers,
                    "tools": tools,
                    "category": category,
                    "query": selected_categories,
                },
            )


def tool_operation(request, id):
    """Функция отображает форму передачи инструмента.
    При получении POST запроса, проверяет наличие товара у получающего владельца,
    если есть добавляет в количество, если нет то создает."""

    tool = get_object_or_404(Tool, id=id)

    if request.method == "POST":
        form = OperationForm(request.POST)

        if form.is_valid():
            form_tool = Tool(
                name=tool.name,
                keeper=tool.keeper,
                description=tool.description,
                price=tool.price,
                quantity=tool.quantity,
                category=tool.category,
            )
            form_tool.quantity = form.cleaned_data["quantity"]
            form_tool.keeper = form.cleaned_data["keeper"]
            # Проверка передачи инструмента более чем есть в наличии и передачи владельцом самому
            # себе. Передача не выполняется и возвращается страница формы.
            if tool.quantity < form_tool.quantity or form_tool.quantity == 0:
                form.add_error(None, "Недостаточно инструмента для передачи")
                return render(request, "store/tool/operation.html", {"tool": tool, "form": form})
            if form_tool.keeper == tool.keeper:
                form.add_error(None, "Производится передача инструмента самому владельцу")
                return render(request, "store/tool/operation.html", {"tool": tool, "form": form})

            tool.quantity = tool.quantity - form_tool.quantity

            try:
                t = Tool.objects.get(name=form_tool.name, keeper=form_tool.keeper, category=tool.category)
                t.quantity += form_tool.quantity
                t.save()
                tool.save()

                operation = Operation.objects.create(
                    giver=tool.keeper, taker=form_tool.keeper, tool=tool, quantity=form_tool.quantity
                )
                operation.save()
                return render(
                    request,
                    "store/tool/detail.html",
                    {
                        "tool": t,
                    },
                )
            except ObjectDoesNotExist:
                tool.save()
                form_tool.save()
                operation = Operation.objects.create(
                    giver=tool.keeper, taker=form_tool.keeper, tool=tool, quantity=form_tool.quantity
                )
                operation.save()
                return render(
                    request,
                    "store/tool/detail.html",
                    {
                        "tool": form_tool,
                    },
                )
    else:
        form = OperationForm()
    return render(
        request,
        "store/tool/operation.html",
        {
            "tool": tool,
            "form": form,
        },
    )
