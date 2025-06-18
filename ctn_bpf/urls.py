from django.urls import path,include
from . import views
# app_name = 'ctn_bpf'
from graphene_django.views import GraphQLView


from rest_framework import routers
router = routers.SimpleRouter()
router.register('boutique',views.InstitutionViewSet,basename='boutique')
router.register('article',views.ArticleViewSet,basename='article')


urlpatterns = [
   path('api/',include(router.urls)),
   path('',views.index,name ='index'),
   path('assistance/',views.assistance,name= 'assistance'),
   path('<int:nature>/',views.index,name ='index_catal'),
   path('admin_institution/',views.admin_institution,name='admin_institution'),
   path('contact/',views.contact,name='contact'),
   path('chaine_indicateurs/',views.chaine_indicateurs,name='chaine_indicateurs'),
   path('edit_institution/<int:institution_id>/',views.edit_institution,name='edit_institution'),
   path('documentation/',views.documentation,name='documentation'),
   path('save_institution/',views.save_institution,name='save_institution'),
   path('save_edit_institution/',views.save_edit_institution,name='save_edit_institution'),
   path('main/',views.main,name='main'),
   path('main/<int:menu_main>/',views.main,name='main_menu'),
   path('bad_auth/',views.bad_auth,name='bad_auth'),
   path('log_account/',views.log_account,name='log_account'),
   path('log/',views.log,name='log'),
   path('log/<int:out>/',views.log,name='log_out'),
   path('log_plus/',views.specific_log,name='specific_log'),
   path('decision/<str:nature>/<int:operation_id>/',views.decision,name='decision'),
   path('decision/<str:nature>/<int:element_id>/<int:operation_rapport_id>/',views.decision,name='decision'),
   path('gestionnaire/<str:gest_val>/',views.gestionnaire,name='gest_val'),
   path('get_indicateur_value/',views.get_indicateur_value,name='indicateur_value'),
   path('gestionnaire/<str:gest_val>/<int:gest_id>/',views.gestionnaire,name='gest_val_id'),
   path('modify/<str:arg_val>/',views.modify,name='modify'),
   path('operations/',views.operations_home,name='operations_home'),
   path('operations/details/<int:operation_id>/',views.operations_details_list,name='operations_details_list'),
   path('operations/<int:operation_id>/',views.operations_details,name='operations_details'),
   path('notifications/',views.notifications,name='notifications'),
   #path('messages/',views.messages,name='messages'),
   path('assign_supervisor/',views.assign_supervisor,name='assign_supervisor'),
   path('valid_rapport/',views.valid_rapport,name='valid_rapport'),
   path('in_valid_rapport/',views.in_valid_rapport,name='in_valid_rapport'),
   path('delete/',views.delete,name='delete'),
   path('delete_mul/',views.delete_mul,name='delete_mul'),
   path('configurations/',views.configurations,name='configurations'),
   path('institution/',views.institutions,name='institution'),
   path('profile/',views.profile,name='profile'),
   path('history/',views.history,name='history'),
   path('history/<str:dates>/',views.history,name='history_dates'),
   path('extra/',views.extra,name="extra"),
   path('save_period/',views.save_period,name='save_period'),
   path('set_period/<int:period>/',views.set_default_period,name='set_session'),
   path('set_institution/<int:institution_id>/',views.set_institution,name='set_institution'),
   path('set_period/<int:period>/<int:sub_period>/',views.set_default_period,name='set_session2'),
   path('consult_oper/',views.consult_oper,name="consult_oper"),
   path('list_tach',views.List,name='List'),
   path('tache_effectuee',views.taches_effectuee,name="tache_effectuee"),
   path('Avis/c/<int:id>',views.Avis,name='Avis'),
   path('Avis/i/<int:id>/',views.Avis_informed,name='Avis'),
   path('recuperer_personnel/',views.recuperer_personnel,name="recuperer_personnel"),
   path('save_design',views.design_form,name="save_design"),
   path('data_sets_edit/<int:id>/',views.edit_dataset,name="data_sets_edit"),
   path('count_operations/',views.count_operations,name="count_operations"),
   path('count_informed/',views.count_informed,name="count_informed"),
   path('count_tache_consulted/',views.count_tache_consulted,name="count_tache_consulted"),
   path('tache_consulted/',views.tache_consulted,name='tache_consulted'),
   path('edit_data/<int:id>',views.edit_data,name="edit_data"),
   path('count_persos/',views.count_persos,name="count_persos"),
   path('count_accountable/',views.count_accountable,name="count_accountable"),
   path('count_effectuee/',views.count_effectuee,name="count_effectuee"),
   path('tache_valide/',views.tach_valid,name="tache_valide"),
   path('soft_delete/<int:id>',views.archive,name="soft_delete"),
   path('tache_archive/',views.archive_list,name="tache_archive"),
   path('soft_deleted/<int:id>',views.restore,name="soft_deleted"),
   path('count_restored/',views.count_restored,name="count_restored"),
   path('save_comment/',views.save_comment,name="save_comment"),
   path('operation_file/<int:id>',views.file,name="operation_file"),
   path('avis_inform/',views.Avis_Informed,name="avis_inform"),
   path('edit_form/<int:id>',views.edit_form,name="edit_form"),
   path('edit_personnel/<int:id>',views.edit_personnel,name="edit_personnel"),
   path('recup_password',views.recup_password,name="recup_password"),
   path('verify/<str:email>',views.verify,name="verify"),
   path('verify_code',views.verify_code,name="verify_code"),
   path('new_password/',views.new_password,name="new_password"),
   path('save_password',views.save_password,name="save_password"),
   path('tache_Attente/',views.tache_attente,name="tache_attente"),
   path('import/', views.import_from_excel, name='import_from_excel'),
   path('historique/',views.historique,name='historique'),
   path('message/',views.message,name="message"),
   path('view/file/<int:id>',views.View_file,name="view_file"),
   path('rejet_rapport/<int:id>',views.rejet_rapport,name="rejet_rapport"),
   path('count_consult/',views.count_consult,name="count_consult"),
   path('View_file_operation/<int:id>/',views.View_file_operation,name="View_file_operation"),
   path('data_set/modif/<int:id>/',views.modif_form,name="data_set"),
   path('error_page/',views.error_page,name="error_page"),
   path('regroup_consulted/',views.regroup_consulted,name="regroup_consulted"),
   path('download_files/<int:id>/',views.download_files,name="download_files"),
   #path('create_indicateurval/',views.create_indicateurval,name="create_indicateurval"),
   path('load_structur/',views.load_file,name="load_structur"),
   path('load_entity/',views.load_entity,name="load_entity"),
   path('licences/',views.licences,name="licences"),
   path('add_license/',views.add_license,name="add_license"),
   path('add_users/',views.add_users,name="add_users"),
   path('archive_doc/',views.archive_doc,name="archive_doc"),
   path('add_categorie/',views.add_categorie,name="add_categorie"),
   path('add_archive/',views.add_archive,name="add_archive"),
   path('convert_to_pdf/',views.convert_to_pdf,name="convert_to_pdf"),
   path('download/<int:id>',views.download,name="download"),
   path('ma_vue/',views.ma_vue,name="ma_vue"),
   path('drop_categorie/<int:id>/',views.drop_categorie,name="drop_categorie"),
   path('edit_categorie/<int:id>/',views.edit_categorie,name="edit_categorie"),
   path('add_souscategory/',views.add_souscategory,name="add_souscategory"),
   path('search_categorie/',views.get_categorie,name="get_categorie"),
   path('drop_sous_categorie/<int:id>/',views.drop_sous_categorie,name="drop_sous_categorie"),
   path('add_archive_operation/<int:operation_id>/',views.add_archive_operation,name="add_archive_operation"),
   path('edit_sous_categorie/<int:id>/',views.edit_sous_categorie,name="edit_sous_categorie"),
   path('edit_souscategory/<int:sous_categorie_id>/',views.edit_souscategory,name="edit_souscategory",),
   path('add_periode/',views.add_periode,name="add_periode"),
   path('get_periodeok_informations/', views.get_periodeok_informations, name='get_periodeok_informations'),
   path('recuperer_donnees_pour_graphique/<int:id>/', views.recuperer_donnees_pour_graphique, name='recuperer_donnees_pour_graphique'),

   path('add_sousactualite/',views.add_sousactualite,name="add_sousactualite"),

   path('trash_sousactualite/<int:id>/',views.trash_sousactualite,name="trash_sousactualite"),

   path('delete_Rubrique/<int:id>/',views.delete_Rubrique,name="trash_actualite"),

   path('valid_actualite/',views.valid_actualite,name="valid_actualite"),

   path('actualite/',views.actualite, name="actualite"),


   path('add_rubrique/',views.add_rubrique,name="add_rubrique"),

   path('view_cible/<int:id>/',views.view_cible,name="view_cible"),

   path('add_cible/',views.add_cible_ajax,name="add_cible_ajax"),

   path('delete_cible/<int:id>/',views.delete_cible,name="delete_cible"),

   path('update_indicateur_valeur/', views.update_indicateur_valeur, name='update_indicateur_valeur'),

   path('journalisation/',views.journalisation,name="journalisation"),


   path('stat_doc/<int:id>/',views.stat_doc,name="stat_doc"),

   path('count_views_document/<int:id>',views.count_views_document,name="count_views_document"),

   path('recuperer_periodes_par_id/',views.recuperer_periodes_par_id,name="recuperer_periodes_par_id"),

   path('recuperer_periodes/',views.recuperer_periodes,name="recuperer_periodes"),

   path('recuperer_periodes_mensuel/',views.recuperer_periodes_mensuel,name="recuperer_periodes_mensuel"),

   path('recuperer_periodes_trimestriel/',views.recuperer_periodes_trimestriel,name="recuperer_periodes_trimestriel"),

   path('recuperer_indicateurs/',views.recuperer_indicateurs,name="recuperer_indicateurs"),

   path('recuperer_nombre_consultations/',views.recuperer_nombre_consultations,name="consultation"),

   path('search_rubrique/',views.search_rubrique,name="search_rubrique"),

   path('view_actualite/<int:id>/',views.view_actualite,name="view_actualite"),

   path('all_actuality/',views.all_actuality,name="all_actuality"),

   path('institution_list/',views.institution_list,name="institution_list"),

   path('archive_operation_rapports/<int:id>/',views.archive_operation_rapports,name="archive_operation_rapports"),

   path('all_actuality_site/',views.all_actuality_site,name="all_actuality_site"),

   path('recuperer_periodes/',views.recuperer_periodes,name="recuperer_periodes"),

   path('search_period/',views.search_period,name='search_period'),
   path('add_sub_structure/',views.add_sub_structure,name="add_sub_structure"),
   
   path('count_informed/',views.count_informed,name="count_informed"),
   
   path('view_file/<int:id>',views.view_file,name="view_file"),
   
   
   path('add_baniere/',views.add_baniere,name="add_baniere"),
   
   path('groupe_institution/',views.groupe_institution,name="groupe_institution"),
   
   
   path('edit_group_institution/<int:id>/',views.edit_group_institution,name="edit_group_institution"),

   path('delete_group/<int:id>/',views.delete_group,name="delete_group"),
   
   path('delete_baners/<int:id>/',views.delete_baners,name="delete_baners"),
   
   path('groupe_link/<int:id>',views.groupe_link,name="groupe_link"),

   path('invoices/',views.invoices,name="invoices"),
   
   path('invoice_fosa/',views.invoice_fosa,name="invoice_fosa"),
   
   path('groupe_element/',views.groupe_element,name="groupe_element"),
   
   path('delete_groupe_element/<int:id>',views.delete_groupe_element,name="delete_groupe_element"),
   
   path('generate_pdf_district/',views.generate_pdf_district,name="generate_pdf_district"),
   
   path('edit_structure/<int:id>/',views.edit_structure,name="edit_structure"),
   
   path('delete_sub_line/<int:id>/',views.delete_sub_line,name="delete_sub_line"),
   
   path('presentation/<int:id>',views.presentation,name="presentation"),
   
   
   path('actualites_del/<int:id>/',views.actualites_del,name="actualites_del"),
   
   path('baniere_actialite/<int:id>/',views.baniere_actialite,name="baniere_actialite"),
   
   path('facturation/',views.facturation,name="facturation"),
   
   path('add_master/',views.add_master,name="add_master"),
   
   path('add_master/',views.add_master,name="add_master"),
   path('delete_master_groupe/<int:id>',views.delete_master_groupe,name="delete_master_groupe"),
   
   path('delete_master/<int:id>/',views.delete_master,name="delete_master"),
   
   path('add_master_element/',views.add_master_element,name="add_master_element"),
   
   path('add_nature/<int:id>/',views.add_nature,name="add_nature"),
   
   path('add_nature_operation/',views.add_nature_operation,name="add_nature_operation"),
   path('configurations_admin/',views.configurations_admin,name="configurations_admin"),
   path('data/',views.data,name="data"),
   path('load_file_data/',views.load_file_data,name="load_file_data"),
   path('activ_cat/<int:id>/',views.activ_cat,name="activ_cat"),
   path('add_categorie_operation/',views.add_categorie_operation,name="add_categorie_operation"),
   path('delete_periode/<int:id>/',views.delete_periode,name="delete_periode"),
   path('desactive_nature/<int:id>/',views.desactive_nature,name="desactive_nature"),
   path('desactive_categorie/<int:id>/',views.desactive_categorie,name="desactive_categorie"),
   path('add_periode/',views.add_periode,name="add_periode"),
   path('api_count_operations_by_nature/',views.api_count_operations_by_nature,name="api_count_operations_by_nature"),
   path('api_count_operations_by_categorie/',views.api_count_operations_by_categorie,name="api_count_operations_by_categorie"),
   path('invoice_district/',views.invoice_district,name="invoice_district"),
   path('analyse_data_indicateur/<int:id>/',views.analyse_data_indicateur,name='analyse_data_indicateur'),
   path('duplicate_dataset/<int:id>/',views.duplicate_dataset,name='duplicate_dataset'),
   path('duplicate_form/',views.duplicate_form,name='duplicate_form'),
   path('data_element/group/',views.data_element_group,name='data_element_group'),
   path('add_groupe_dataelement/',views.add_groupe_dataelement,name='add_groupe_dataelement'),
   path('add_all_group/',views.add_all_group,name='add_all_group'),
   path('indicator_group/',views.indicator_group,name='indicator_group'),
   path('add_groupe_indicateur/',views.add_groupe_indicateur,name='add_groupe_indicateur'),

   path('add_all_group_indicateur/',views.add_all_group_indicateur,name='add_all_group_indicateur'),

   path('delete_entities/<int:id>/',views.delete_entities,name='delete_entities'),
   path("graphql/", GraphQLView.as_view(graphiql=True)),
   path('add_structure/',views.add_structure,name='add_structure'),

   path('edit_periode/<int:id>/',views.edit_periode,name='edit_periode'),

  path('edition_periode/<int:id>/',views.edition_periode,name='edition_periode'),
  path('roles_personnels/',views.roles_personnels,name='roles_personnels'),

  path('add_sou_rubrique/<int:id>/',views.add_sou_rubrique,name='add_sou_rubrique'),

  path('deleted_personnel/<int:id>/',views.deleted_personnel,name='deleted_personnel'),
  path('calculators_operations/',views.calculators_operations,name='calculators_operations'),


  path('api_count_operations/',views.api_count_operations,name='api_count_operations'),

  path('api_get_categories/',views.api_get_categories,name='api_get_categories'),

  path('edit_indicator/<int:id>/',views.edit_indicator,name='edit_indicator'),
  path('editions_indicator/<int:id>/',views.editions_indicator,name='editions_indicator'),
  path('participant/',views.template_participant,name='participant'),

  path('count_participant/',views.count_participant,name='count_participant'),

  path('affecter_operation/<int:id>/',views.affecter_operation,name='affecter_operation'),
  path('edit_role/<int:id>/',views.edit_role,name='edit_role'),
  path('delete_role/<int:id>/',views.delete_role,name='delete_role'),

  path('view_actuality/<int:id>/',views.view_actuality,name='view_actuality'), 
  path('add_faq/',views.add_faq,name='add_faq'),
  path('sousActuality/<int:id>/',views.sousActuality,name='sousActuality'),

  path('view_actualitys/<int:id>/<int:id2>/',views.view_actualitys,name='view_actualitys'),

  path('initial_command/<int:id>/',views.initial_command,name='initial_command'),

  path('article_detail/<int:id>/',views.article_detail,name='article_detail'),



  path('dashboard/e-commerce/',views.dashboard_ecommerce,name='dashboard'),
  path('register/',views.register,name='register'),

  path('login_ecommerce/',views.login_ecommerce,name='login_ecommerce'),
  path('add_personnel/',views.add_personnel,name='add_personnel'),
  path('boutique/',views.boutique,name='boutique'),

  path('save_institute/',views.save_institute,name='save_institute'),
  path('add_partner/',views.add_partner,name='add_partner'),
  path('select_rubrique/',views.select_rubrique,name='select_rubrique'),

  path('articles/institution/<int:id>/<int:id2>/',views.articles_institution,name='articles'),
   


 
]
gestionnaire_url_patterns = [
   path('duplicate/',views.duplicate,name='duplicate'),
   path('structures/',views.structures,name='structures'),
   path('personnels/',views.personnels,name='personnels'),
   path('perso/<int:perso_id>/',views.personnel_id,name='personnels_details'),
   path('personnels_raci/',views.personnels_raci,name='personnels_raci'),
   path('users_simples/',views.users_simples,name='users_simples'),

   path('structures/',views.structures,name='structures'),
   path('dataelts/',views.dataelts,name='data_elets'),
   path('dataelts/<int:elt_id>/',views.dataelts,name='data_elets_id'),
   path('dataelts/<int:elt_id>/<int:elt_str>/',views.dataelts,name='data_elets_id2'),
   path('dataelts/indic/',views.dataelts_indic,name='data_elets_indic'),
   path('dataelt/edit/<int:elt_id>/',views.dataelts_edit,name='data_elets'),
   path('data_elements/',views.data_elements,name='data_elements'),
   path('data_sets/<int:indi_id>/',views.data_sets,name='data_sets'),
   path('data_sets/design/<int:dS_id>/',views.data_sets_design,name='data_sets'),

   path('data_form/<str:nature>/<int:elt_id>/',views.data_form,name="data_form"),
   path('roles/',views.roles,name='roles'),
	path('taches/<int:tache_id>/',views.ges_taches,name='ges_taches'),
   path('taches/<int:tache_id>/<int:arg_period>/',views.ges_taches,name='ges_taches'),
   path('alert_notifs/<str:tree>/<int:report>/',views.alert_notifs,name='alert_notifs'),
   path('add_cat_nat/<int:id>/',views.add_cat_nat,name="add_cat_nat"),
   
   path('count_attente_operation/',views.count_attente_operation,name="count_attente"),
   
   path('activ_form/<int:id>/',views.activ_form,name="activ_form"),
   path('add_sous_actualite/',views.add_sous_actualite,name="add_sous_actualite"),
   path('delete_sous_actualite/<int:id>/',views.delete_sous_actualite,name="delete_sous_actualite"),
   
   path('edit_baniere_institution/',views.edit_baniere_institution,name="edit_baniere_institution"),
   path('get_dataset/<int:dataset_id>/',views.get_dataset,name="ajax_form_2"),
   
   path('access_website/<int:id>/',views.actual,name="actual"),
   path('edit_sous_actualite/<int:id>/',views.edit_sous_actualite,name="edit_sous_actualite"),
   path('update_sous_actuality/<int:id>/',views.update_sous_actuality,name="update_sous_actuality"),
   path('edit_baniere/<int:id>/',views.edit_baniere,name="edit_baniere"),
   path('edit_baniere_up/<int:id>/',views.edit_baniere_up,name="edit_baniere_up"),
   path('delete_nature/<int:id>/',views.delete_nature,name="delete_nature"),
   path('delete_categorie/<int:id>/',views.delete_categorie,name="delete_categorie"),
   path('get_dataset_accountable/<int:id>/',views.get_dataset_accountable,name="get_dataset_accountable"),
   path('save_value/',views.save_value,name="save_value"),
   path('load_data/<int:structure_id>/<int:periode_id>/', views.load_data,name='load_data'),
   path('toggle_public/',views.toggle_public,name='toggle_public'),  
   path('delete_institution/<int:id>/',views.delete_institution,name='delete_institution'),
   path('dataset_load/<int:id>/<int:operation_id>/',views.dataset_load,name='dataset_load'),
   path('calendar/',views.calendar,name='calendar'),
   path('api_operations/',views.get_operations,name='get_operations'),
   path('line_delete_structure/<int:id>/',views.line_delete_structure,name='line_delete_structure'),

   path('gantt/',views.gantt,name='gantt'),


   path('clone_operations/<int:id>/',views.file_duplik,name='duplicate_operation'),

   path('duplicate_operation/<int:id>/',views.duplicate_operation,name='duplicate_operation'),
   path('forms_data/',views.forms_data,name='forms_data'),
   # path('set_language/', views.set_language, name='set_language'),
   path('delete_indicateur/<int:id>/',views.delete_indicateur,name='delete_indicateur'),

   path('add_groupe_indicateur/',views.add_groupe_indicateur,name='add_groupe_indicateur'),

   path('Associer_groupe_indicateur/<int:id>/',views.Associer_groupe_indicateur,name='Associer_groupe_indicateur'),

   # path('add_masters_indicateur/',views.add_masters_indicateur,name='add_masters_indicateur'),
   path('add_groupe_structure/',views.add_groupe_structure,name='add_groupe_structure'),
   path('list_element/<int:id>/',views.list_element,name='list_element'),
   path('list_indicator_group/<int:id>/',views.list_indicator_group,name='list_indicator_group'),
   path('delete_group_indicator/<int:id>/',views.delete_group_indicator,name='delete_group_indicator'),

   path('delete_groupe_element/<int:id>/',views.delete_groupe_element,name='delete_groupe_element'),

   path('delete_data_element/<int:id>/',views.dataelt,name='dataelt'),
   path('loaddata_set/<int:id>/<int:operation_id>/',views.loaddata_set,name='loaddata_set'),
   path('groupe_structure/',views.groupe_structure,name='groupe_structure'),

   path('add_forms/<int:id>/',views.add_forms,name='add_forms'),
   
   path('add_periodes/', views.MonFormulaireView.as_view(), name='ton_view_name'),  
   path('delete_periodes/<int:id>/',views.Deletes_periodes.as_view(),name='deletes_periodes'),

   path('add_dataset_institution/<int:id>/',views.add_dataset_institution,name='add_dataset_institution'),
   path('account/<int:id>/',views.account,name='account'),

   path('actualites_modif/<int:id>/',views.actualites_modif,name='actualites_modif'),
   path('edition_actualite/<int:id>/',views.edition_actualite,name='edition_actualite'),

   path('all_article/<int:id>/',views.all_article,name='all_article'),

   path('sous_articles/institution/<int:id>/<int:id2>/',views.sous_articles,name='sous_articles'),
   path('all_actuality_article/<int:id>/',views.all_actuality_article,name='all_actuality_article'),

   path('espace/',views.espace_vendeur,name='espace'),

   path('Mdp_Dart/',views.Mdp_Dart,name='Mdp_Dart'),
   path('api/articles/filter/', views.get_articles, name='get_articles'),
   path('recherche/suggestions/',views.search_suggestions,name='search_suggestions'),

   path('logout_view/',views.logout_view,name='logout_view'),

   path('boutique/<str:slug>/', views.boutique_detail, name='boutique_detail'),
]
ajax_urls_patterns = [
   path('count_notifs/',views.notifs,name='notifs'),
   path('count_rapps/',views.notifs_rapp,name='notifs_rapp'),
   path('count_indic/',views.indicateurs_ajax,name='indicateur_ajax'),
   path('ajax_graphiques/',views.ajax_graphiques,name='ajax_graphiques'),
   path('ajax_lines/',views.ajax_lines,name='ajax_lines'),
   path('get_elements/',views.get_elements,name='get_elements'),
   path('get_elements_hierachy/',views.get_elements_hierachy,name='get_elements_hierachy'),
   path('get_elements_subsequency/',views.get_elements_subsequency_true,name='get_elements_subsequency_true'),
   path('get_indi_data/',views.get_indi_data,name='get_indi_data'),
   path('ajax_restore/',views.ajax_restore,name='ajax_restore'),
   path('ajax_institution/',views.ajax_institution,name='ajax_institution'),
   path('print_pdf/',views.print_pdf,name='print_pdf'),
   path('ajax_progress/',views.ajax_progression,name='ajax_progress'),
   path('get_progressions/',views.get_progressions,name='get_progressions'),
   path('ajax_calcul_date/',views.ajax_calcul_date,name='ajax_calculate_date'),
   path('ajax_form/',views.ajax_form,name='ajax_form'),
   path('ajax_RACI_user/',views.ajax_RACI_user,name='ajax_RACI_user'),
   path('ajax_RACI_user/manage/',views.ajax_RACI_user_manage,name='ajax_RACI_user'),
   path('ajax_hiera_struc/',views.ajax_hiera_struc,name='ajax_hiera_strux'),
   path('update_categorie/<int:id>/',views.update_categorie,name="update_categorie"),
   path('edit_natures/<int:id>/',views.edit_natures,name="edit_natures"),
   path('edit_categorie_up/<int:id>/',views.edit_categorie_up,name="edit_categorie_up"),
   path('edit_nature_up/<int:id>/',views.edit_nature_up,name="edit_nature_up"),
   path('add_information_actualite/<int:id>/',views.add_information_actualite,name="add_information_actualite"),
   path('add_information_data/<int:id>/',views.add_information_data,name="add_information_data"),

   path('add_nature_indicateur/',views.add_nature_indicateur,name='add_nature_indicateur'),
   path('data_sets_duplicate/<int:id>/',views.data_sets_duplicate,name='data_sets_duplicate'),

   path('delete_selected_operations/',views.delete_selected_operations,name='delete_selected_operations'),

   path('view_reult/<int:id>/',views.view_reult,name='view_reult'),

   path('settings/',views.settings,name='settings'),
   path('groupe_boutique/',views.groupe_boutique,name='groupe_boutique'),
   path('villes/',views.villes,name='villes'),
   path('rubriques/',views.rubriques,name='rubriques'),
   path('all_market/',views.all_market,name='all_market'),
   path('edit_groupe_institution/<int:id>/',views.edit_groupe_institution,name='edit_groupe_institution'),

   path('edition/<int:id>/',views.edition,name='edition'),

   path('edit_boutique/<int:id>/',views.edit_boutique,name='edit_boutique'),
   path('profil/',views.profil,name='profil'),
   path('support/',views.support,name='support'),
   
]
save_url_patterns = [
   path('save_entity/',views.save_entity,name='save_entity'),
   path('save_entity_value/',views.save_entity_value,name='save_entity_value'),
   path('save_indicateur/',views.save_indicateur,name='save_indicateur'),
   path('save_gestion/',views.save_gestion,name='save_gestion'),
   path('save_plannify/',views.save_plannify,name='save_plannify'),
   path('save_rapport/',views.save_rapport,name='save_rapport'),
   path('save_valid_rapport/',views.save_valid_rapport,name='save_valid_rapport'),
   path('valid_observations/',views.valid_observations,name='valid_observations'),
   path('assign_RACI/',views.assign_RACI,name='assign_RACI')
]

filter_urls = [
   path('filter_op/',views.filter_op,name='filter_op'),
   path('filter_entity/',views.filter_entities,name='filter_entities'),
   path('gestionnaire_search/',views.gestionnaire_search,name='gestionnaire_search'),
   path('search/',views.search,name='search'),
   path('search2/<str:menu>/',views.search2,name='search2'),
   path('filter_op/search/',views.filter_op_search,name='filter_op'),
   path('filter_perso/<int:structure_id>/<int:role_id>/',views.filter_perso,name='filter_perso'),
   path('structures/<int:structure_id>/',views.structure_details,name='structure_details'),
   path('structures_hie/',views.structure_hie,name='structure_details_f'),
   path('evaluer/<str:hierachie>/',views.evaluer,name='evaluer'),
   path('evaluer/<str:hierachie>/<int:gest_id>/',views.evaluer,name='evaluer'),
   path('evaluer_detail/<int:gest_id>/',views.evaluer_detail,name='evaluer_detail'),
   path('indic/<int:indic_id>/',views.indic_plus,name='indic_plus'),
   path('search_period_id/',views.search_period_id,name='search_period_id'),

   path('grub_form/<int:id>/',views.grub_form,name='grub_form'),
   path('gantt_planification/',views.gantt_planification,name='gantt_planification')
   
]

# Ajouter Journal RACI

log_urls = [
   path('messengers/',views.messengers,name="messengers"),

   path('bad_pass/',views.bad_pass,name='bad_pass'),
   path('restorepass/',views.restorepass,name='restorepass'),
   path('print_mail_file/',views.print_mail_file,name='print_file'),
   path('agenda/',views.agenda,name='agenda'),
   path('genPDF/',views.print_pdf,name="gen_PDF")
]
urlpatterns += ajax_urls_patterns
urlpatterns += gestionnaire_url_patterns
urlpatterns += save_url_patterns
urlpatterns += filter_urls
urlpatterns += log_urls
#path('calendar/',views.calendar,name='calendar'),
