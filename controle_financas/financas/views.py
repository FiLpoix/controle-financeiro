from django.shortcuts import render, redirect
from .models import Transacao, Categoria
from .forms import TransacaoForm
from django.db.models import Sum
from datetime import date
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Função para renderizar gráficos
def gerar_grafico():
    categorias = Categoria.objects.all()
    dados = {categoria.nome: Transacao.objects.filter(categoria=categoria).aggregate(Sum('valor'))['valor__sum'] or 0
             for categoria in categorias}

    fig, ax = plt.subplots()
    ax.pie(dados.values(), labels=dados.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    grafico = base64.b64encode(buffer.read()).decode('utf-8')
    return grafico

# Lista de transações
def lista_transacoes(request):
    transacoes = Transacao.objects.all()
    saldo = transacoes.aggregate(Sum('valor'))['valor__sum'] or 0
    grafico = gerar_grafico()

    return render(request, 'financas/lista_transacoes.html', {
        'transacoes': transacoes,
        'saldo': saldo,
        'grafico': grafico
    })

# Cadastro de transação
def cadastrar_transacao(request):
    if request.method == 'POST':
        form = TransacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_transacoes')
    else:
        form = TransacaoForm()
    
    return render(request, 'financas/cadastro_transacao.html', {'form': form})

# Filtro por período
def filtrar_transacoes(request):
    if request.method == 'POST':
        mes_inicio = int(request.POST.get('mes_inicio', 1))
        ano_inicio = int(request.POST.get('ano_inicio', 2020))
        mes_fim = int(request.POST.get('mes_fim', 12))
        ano_fim = int(request.POST.get('ano_fim', 2023))

        transacoes = Transacao.objects.filter(
            data__month__gte=mes_inicio, data__year__gte=ano_inicio,
            data__month__lte=mes_fim, data__year__lte=ano_fim
        )

        saldo = transacoes.aggregate(Sum('valor'))['valor__sum'] or 0
        grafico = gerar_grafico()

        return render(request, 'financas/lista_transacoes.html', {
            'transacoes': transacoes,
            'saldo': saldo,
            'grafico': grafico
        })

    return render(request, 'financas/filtro_periodo.html')