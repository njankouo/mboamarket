from django.urls import path
from . import views
app_name = 'ctn_bpf'
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
urlpatterns = [
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

   path('change_language/<str:language_code>/', views.change_language, name='change_language'),


   path('activ_ponderation/<int:id>/',views.add_ponderation,name="add_ponderation")
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

   path('rapport_declare/',views.rapport_declare,name="rapport_declare"),

   path('count_declare/',views.count_declare,name="count_declare"),

   path('count_declare_d2/',views.count_declare_d2,name="count_declare_d2")

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
   path('indic/<int:indic_id>/',views.indic_plus,name='indic_plus')
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
