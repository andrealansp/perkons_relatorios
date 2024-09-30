from decouple import config
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView

from app.common.jira_handling import JiraHandling
from preventiva.forms import PreventivaForm
import logging

logger = logging.getLogger("preventivas")


class PreventivasView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    template_name = 'preventivas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estatistica'] = self.get_statistics_data()
        return context

    def get_statistics_data(self):
        jira_context = JiraHandling(config("URL"), config("USER_JIRA"), config("API_TOKEN"), config("CAMPOS_PCLS"))
        jira_context.set_jql("perkons-preventivas-pcls-mes")
        return jira_context.get_statistic_preventive()


class PerkonsFormView(LoginRequiredMixin, FormView):
    login_url = '/accounts/login/'
    form_class = PreventivaForm
    template_name = 'preventivas_handling.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Visualizar Preventivas Perkons"
        return context

    def form_valid(self, form):
        di = form.cleaned_data["data_inicial"]
        df = form.cleaned_data["data_final"]
        logger.info(f"O usuário:{self.request.user} Gerou o relatório para as datas: {di} - {df} !")
        return HttpResponseRedirect(reverse('perkons_relatorio', kwargs={'di': di, 'df': df}))


class PerkonsRelatorioTemplateView(TemplateView):
    template_name = 'perkons_report.html'
    context_object_name = "chamados"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chamados'] = self.get_issues_jira()
        return context

    def get_issues_jira(self):
        jira_context = JiraHandling(config("URL"), config("USER_JIRA"), config("API_TOKEN"), config("CAMPOS_PCLS"))
        jira_context.set_jql("perkons-preventivas-pcls", self.kwargs['di'], self.kwargs['df'])
        return jira_context.getissues()


class VelsisFormView(LoginRequiredMixin, FormView):
    login_url = '/accounts/login/'
    form_class = PreventivaForm
    template_name = 'preventivas_handling.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Visualizar Preventivas Velsis"
        return context

    def form_valid(self, form):
        di = form.cleaned_data["data_inicial"]
        df = form.cleaned_data["data_final"]
        logger.info(f"O usuário:{self.request.user} Gerou o relatório para as datas: {di} - {df} !")
        return HttpResponseRedirect(reverse('velsis_relatorio', kwargs={'di': di, 'df': df}))


class VelsisRelatorioTemplateView(TemplateView):
    template_name = 'velsis_report.html'
    context_object_name = "chamados"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chamados'] = self.get_issues_jira()
        return context

    def get_issues_jira(self):
        jira_context = JiraHandling(config("URL"), config("USER_JIRA"), config("API_TOKEN"), config("CAMPOS_VELSIS"))
        jira_context.set_jql("velsis-preventivas-balancas", self.kwargs['di'], self.kwargs['df'])
        return jira_context.getissues()


class SalasFormView(LoginRequiredMixin, FormView):
    login_url = '/accounts/login/'
    form_class = PreventivaForm
    template_name = 'preventivas_handling.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Visualizar Preventivas Salas de Operação"
        return context

    def form_valid(self, form):
        di = form.cleaned_data["data_inicial"]
        df = form.cleaned_data["data_final"]
        logger.info(f"O usuário:{self.request.user} Gerou o relatório para as datas: {di} - {df} !")
        return HttpResponseRedirect(reverse('salas_relatorio', kwargs={'di': di, 'df': df}))


class SalasRelatorioTemplateView(TemplateView):
    template_name = 'salas_report.html'
    context_object_name = "chamados"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chamados'] = self.get_issues_jira()
        return context

    def get_issues_jira(self):
        jira_context = JiraHandling(config("URL"), config("USER_JIRA"), config("API_TOKEN"), config("CAMPOS_SALAS"))
        jira_context.set_jql("perkons-preventivas-salas", self.kwargs['di'], self.kwargs['df'])
        return jira_context.getissues()