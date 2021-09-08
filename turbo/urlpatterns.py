#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：carrera 
@File    ：urlpatterns.py
@Author  ：宇宙大魔王
@Date    ：2021/6/11 15:50 
@Desc    ：
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from utils.token.handler import APITokenObtainPairView, APITokenRefreshView
from accounts.views import UserListViewSet, MyGroupUserViewSet, UserDevelopmentDetail, MyTaskBar, MyMcl, MyPcl, \
    MyApproval, MyConfirm, MyRelease, UpdatePassword, UpdateEmailDays, UpdateAvatar
from liaisons.views import LiaisonsViewSet, LiaisonUpdateStatusViewSet, QaProjectDetailViewSet, \
    QaProjectForMineViewSet, QaProjectForGroupViewSet, LiaisonFileUpload, QaProjectDetailView, SyncLiaisonBySirNo, \
    QaProjectDataStatisticsViewSet, AllLiaisonsViewSet
from qa.views import MCLQaHeadViewSet, QaDetailViewSet, QaDetailUpdateResultViewSet, \
    QaDetailUpdateContentTextViewSet, QaHeadUpdateObjectSummaryViewSet, QaHeadModifyDetailViewSet, \
    QaHeadTargetAndActualViewSet, CkEditorImageUpload, CkEditorFileUpload, RecoverFile, PCLQaClass1ViewSet, \
    PCLQaClass2ViewSet, PCLCommitJudgment, TestResultDefaultOK, QaDetailApprovalContentTextViewSet, \
    QadfProofContentTextViewSet, CodeReviewInspection, QaSlipNoCheckOutObject, BatchNewQaDetail
from reviews.views import DesignReviewViewSet, CodeReviewViewSet
from systems.views import SystemsViewSet
from projects.views import ProjectsViewSet
from reports.views import ReportListViewSet, ReportLiaisonListViewSet, ReportLiaisonInfo, ReportQaInfo, ReportOrderInfo, \
    ReportLiaisonPCLViewSet
from rbac.views import WorkingOrganization, WorkingProject
from checkouts.views import CheckOutFilesViewSet, SendEmail

account_router = DefaultRouter()
account_router.register('user_list', UserListViewSet, basename='user_list')
account_router.register('group_users', MyGroupUserViewSet, basename='group_users')

liaison_router = DefaultRouter()
liaison_router.register('liaisons', LiaisonsViewSet, basename='liaisons')
liaison_router.register('all_liaisons', AllLiaisonsViewSet, basename='all_liaisons')
liaison_router.register('liaison_update_status', LiaisonUpdateStatusViewSet, basename='liaison_update_status')
liaison_router.register('qa_project_detail', QaProjectDetailViewSet, basename='qa_project_detail')
liaison_router.register('qa_project_mine', QaProjectForMineViewSet, basename='qa_project_mine')
liaison_router.register('qa_project_group', QaProjectForGroupViewSet, basename='qa_project_group')
liaison_router.register('qa_test_statistics', QaProjectDataStatisticsViewSet, basename='qa_test_statistics')

qa_router = DefaultRouter()
qa_router.register('mcl_head', MCLQaHeadViewSet, basename='mcl_head')
qa_router.register('mcl_head_update_summary', QaHeadUpdateObjectSummaryViewSet, basename='mcl_head_update_summary')
qa_router.register('mcl_head_modify_detail', QaHeadModifyDetailViewSet, basename='mcl_head_modify_detail')
qa_router.register('mcl_head_target_actual', QaHeadTargetAndActualViewSet, basename='mcl_head_target_actual')
qa_router.register('mcl_detail', QaDetailViewSet, basename='mcl_detail')
qa_router.register('pcl_class1', PCLQaClass1ViewSet, basename='pcl_class1')
qa_router.register('pcl_class2', PCLQaClass2ViewSet, basename='pcl_class2')
qa_router.register('mcl_detail_update_result', QaDetailUpdateResultViewSet, basename='mcl_detail_update_result')
qa_router.register('mcl_detail_update_content_text', QaDetailUpdateContentTextViewSet,
                   basename='mcl_detail_update_content_text')
qa_router.register('mcl_detail_approval_content_text', QaDetailApprovalContentTextViewSet,
                   basename='mcl_detail_approval_content_text')
qa_router.register('mcl_detail_proof_content_text', QadfProofContentTextViewSet,
                   basename='mcl_detail_proof_content_text')
qa_router.register('qa_slip_no_checkout_object', QaSlipNoCheckOutObject,
                   basename='qa_slip_no_checkout_object')

checkout_router = DefaultRouter()
checkout_router.register('pb_file_checkout', CheckOutFilesViewSet, basename='pb_file_checkout')

review_router = DefaultRouter()
review_router.register('qa/design_review', DesignReviewViewSet, basename='design_review')
review_router.register('qa/code_review', CodeReviewViewSet, basename='code_review')

master_router = DefaultRouter()
master_router.register('projects', ProjectsViewSet, basename='projects')
master_router.register('systems', SystemsViewSet, basename='systems')

report_router = DefaultRouter()
report_router.register('reports', ReportListViewSet, basename='reports')
report_router.register('list', ReportLiaisonListViewSet, basename='report_list')
report_router.register('list_pcl', ReportLiaisonPCLViewSet, basename='report_list_pcl')

conf_urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('docs/', include_docs_urls(title="drf docs")),
]

common_urlpatterns = [
    path('login/', APITokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', APITokenRefreshView.as_view(), name='token_refresh_pair'),
]

account_urlpatterns = [
    path('', include(account_router.urls)),
    path('mine_order_info/', UserDevelopmentDetail.as_view()),
    path('mine_task_bar/', MyTaskBar.as_view()),
    path('mine_task_mcl/', MyMcl.as_view()),
    path('mine_task_pcl/', MyPcl.as_view()),
    path('mine_task_approval/', MyApproval.as_view()),
    path('mine_task_conform/', MyConfirm.as_view()),
    path('mine_task_release/', MyRelease.as_view()),
    path('update_password/', UpdatePassword.as_view()),
    path('update_email_days/', UpdateEmailDays.as_view()),
    path('update_avatar/', UpdateAvatar.as_view()),
]

liaison_urlpatterns = [
    path('', include(liaison_router.urls)),
    path('liaison_file_upload/', LiaisonFileUpload.as_view()),
    path('qa_project_detail_view/', QaProjectDetailView.as_view()),
    path('sync_sir/', SyncLiaisonBySirNo.as_view()),
]

qa_urlpatterns = [
    path('', include(qa_router.urls)),
    path('image_upload/', CkEditorImageUpload.as_view()),
    path('file_upload/', CkEditorFileUpload.as_view()),
    path('liaison_file_upload/', LiaisonFileUpload.as_view()),
    path('pcl_commit_judgment/', PCLCommitJudgment.as_view()),
    path('files/<str:filename>', RecoverFile.as_view()),
    path('default_ok/', TestResultDefaultOK.as_view()),
    path('codereview_inspection/', CodeReviewInspection.as_view()),
    path('batch_new_qa_detail/', BatchNewQaDetail.as_view()),
]

checkout_urlpatterns = [
    path('', include(checkout_router.urls)),
    path('send_email/', SendEmail.as_view()),
]

rbac_urlpatterns = [
    path('working_organization/', WorkingOrganization.as_view()),
    path('working_project/', WorkingProject.as_view())
]

report_urlpatterns = [
    path('', include(report_router.urls)),
    path('liaison_info/', ReportLiaisonInfo.as_view()),
    path('qa_info/', ReportQaInfo.as_view()),
    path('order_info/', ReportOrderInfo.as_view()),
]

review_urlpatterns = [
    path('', include(review_router.urls))
]

master_urlpatterns = [
    path('', include(master_router.urls))
]

api_urlpatterns = [
    path('', include(common_urlpatterns)),
    path('', include(conf_urlpatterns)),
    path('account/', include(account_urlpatterns)),
    path('liaison/', include(liaison_urlpatterns)),
    path('qa/', include(qa_urlpatterns)),
    path('review/', include(review_urlpatterns)),
    path('master/', include(master_urlpatterns)),
    path('report/', include(report_urlpatterns)),
    path('rbac/', include(rbac_urlpatterns)),
    path('checkout/', include(checkout_urlpatterns))
]
