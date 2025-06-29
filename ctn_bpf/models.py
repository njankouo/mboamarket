# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from .utilities import get_period_values,set_pv_tp,subperiods_value
#import datetime
from datetime import date, datetime, timedelta
import uuid
# from auditlog.models import AuditlogHistoryField
# from auditlog.registry import auditlog
class Owner(models.Model):
	m_user = models.OneToOneField(User,blank=True,null=True,on_delete=models.CASCADE)
	m_code = models.CharField(max_length=128,blank=True,null=True)
	m_bought = models.BooleanField(default=False,blank=True,null=True)
	m_type = models.IntegerField(default=1,blank=True,null=True)
	m_mail_notified = models.BooleanField(default=False,blank=True,null=True)
	def nb_institutions(self):
		return Institution.objects.filter(owner__id=self.id).count()
	def __str__(self):
		return str(self.m_user)

class Periode(models.Model):
	m_value = models.CharField(max_length=128,blank=True,null=True)
	m_decoupage = models.TextField(blank=True,null=True)
	m_decoupage_description	 = models.TextField(blank=True,null=True)
	m_date_creation = models.DateTimeField(db_index=True,auto_now_add=True,blank=True,null=True)
	m_config = models.BooleanField(blank=True,null=True)
	m_initial = models.BooleanField(blank=True,null=True)
	m_logic_type = models.IntegerField(blank=True,null=True)#1 - Jour | 2 - Semaine | 3 - Mois | 9 - Trimestre | 6 - Semestre
	m_code_type = models.TextField(blank=True,null=True)
	def __str__(self):
		return str(self.m_value)
	def sub_periods(self):
		return SubPeriode.objects.filter(m_periode__id=self.id)
	def decoup_slip(self):
		return self.m_decoupage.split("|")
	def decoup_slip_reverse(self):
		tmp = self.decoup_slip()
		if tmp != None:
			tmp = tmp[::-1]
		return tmp
	class Meta:
		ordering=('m_value',)

class SubPeriode(models.Model):
	m_periode = models.ForeignKey(Periode,blank=True,null=True,on_delete=models.CASCADE)
	m_sub_value = models.CharField(max_length=128,blank=True,null=True)
	m_decoupage = models.TextField(blank=True,null=True)
	m_decoupage_description	 = models.TextField(blank=True,null=True)
	m_config_type = models.IntegerField(blank=True,null=True)

	def __str__(self):
		return str(self.m_periode) + " - " + str(self.m_sub_value)
	def decoup_desc_slip(self):
		return self.m_decoupage_description.split("|")
	def decoup_desc_slip2(self):
		return self.m_decoupage.split("|")
# ============ SUPER CLASS ============
class Groupe_institution(models.Model):
    icone=models.FileField(max_length=255,null=True,blank=True)
    nom= models.CharField(max_length=255,null=True,blank=True)
    description=models.TextField(null=True,blank=True)

class Baniere(models.Model):
    nom = models.CharField(max_length=255,null=True,blank=True)
    
    logo = models.FileField(null=True,blank=True)

class Institution(models.Model):
    
	sigle = models.CharField(max_length=255,blank=True,null=True)
	nom = models.CharField(max_length=255)
	date_creation = models.DateTimeField(db_index=True,auto_now_add=True)
	img = models.FileField(blank=True,null=True)
	purpose  = models.TextField(blank=True,null=True)
	address  = models.CharField(blank=True,null=True,max_length=255)
	country  = models.CharField(blank=True,null=True,max_length=255)


	owner = models.ForeignKey(Owner,on_delete = models.SET_NULL,blank=True,null=True)
	default_period = models.ForeignKey(Periode,on_delete = models.SET_NULL,blank=True,null=True)
 
	default_subperiod = models.ForeignKey(SubPeriode,on_delete = models.SET_NULL,blank=True,null=True)
	structures_roles = models.TextField(default="Responsible|Accountable|Consulted|Informed")

	default_options = models.BooleanField(default=False,blank=True,null=True)
	finan_options = models.CharField(max_length=32,blank=True,null=True,default="Franc CFA")#FCFA. $, €
	default_struc_name = models.CharField(max_length=128,blank=True,null=True,default="Structure")
	groupe= models.ForeignKey(Groupe_institution,null=True,blank=True,on_delete=models.CASCADE)
	# The code `repeat_mode` is not a valid Python code snippet. It seems like it might be a variable or
	# function name, but without any context or code surrounding it, it is difficult to determine its
	# purpose or functionality. Can you provide more information or context so I can better understand
	# what you are trying to achieve with this code?
	repeat_mode = models.BooleanField(default=True,blank=True,null=True)
 	
	ponderation = models.BooleanField(null=True,default=False,blank=True)
	link = models.URLField(null=True, blank=True)
	nature=models.CharField(null=True,blank=True,default=True,max_length=255)
	categorie_op=models.BooleanField(null=True,default=True,blank=True)
	baniere = models.ForeignKey(Baniere,on_delete=models.CASCADE,null=True)
	formulaire=models.BooleanField(null=True,default=True)

	is_social_media = models.BooleanField(default=True)
	numero_whatsapp = models.TextField()
	
	lien_facebook = models.URLField()
	lien_instagram = models.URLField()
	hash_code = models.CharField(null=True,max_length=255)
	status = models.IntegerField(null=True,default=1)
	description = models.TextField(null=True)
	#id = models.AutoField(primary_key=True)
	#uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	email = models.CharField(null=True,blank=True,max_length=255)

	parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
	partenaires = models.ManyToManyField('self', symmetrical=True, blank=True)  # Relation many-

	accept = models.BooleanField(default=False)
   
	def __str__(self):
		if self.sigle != None:
			return self.sigle
		else:
			return self.nom

	def Structure_Hierachy(self):
		return [Structure_Hierachy.objects.filter(m_institution__id=self.id).first()]

	def structures(self):
		return Structure.objects.filter(institution__id=self.id)

	def structures_not_null(self):
		result = list()
		for s in self.structures():
			if s.taches().first() != None:
				result.append(s)
		return result

	def structures_split(self):
		return self.structures_roles.split('|')

	def funtions(self):
		return Personnel_Function.objects.filter(m_institution__id=self.id).select_related('m_institution')

	def periodes(self):
		return Institution_Periodes.objects.filter(m_institution__id=self.id).select_related('m_institution')

	def get_entities(self):
		result = InsitutionEntities.objects.filter(m_institution__id = self.id).select_related('m_institution')
		return result

	def top_entity(self):
		tmp = self.get_entities().first().m_entity_type
		return tmp

	def last_entity(self):
		return self.get_entities().last().m_entity_type

	def taches(self):
		return self.last_entity().lines()

	def finances(self):
		taches = self.last_entity().lines()
		result = 0
		for t in taches:
			if t.montant != None:
				result += t.montant
		return result

	def depenses_eff(self):
		operations = Operation.objects.filter(m_institution=self.id).values('montant2')
		result = 0
		for o in operations:
			if o["montant2"] != None:
				result+=o["montant2"]
		return result

	def progression(self,period=None):
		result = 0
		i = 0
		"""
		top_entity = self.top_entity()
		bool(top_entity)

		programmes = top_entity.lines()
		bool(programmes)

		for p in programmes:
			result += p.progression()
			i += 1
		if i > 0:
			result = round((result/i),2)
		"""
		operations = Operation.objects.filter(m_institution=self.id)#.values('etat')
		bool(operations)
		i = 0
		for o in operations:
			result += o.progression()#(100 if (o["etat"])=='2' else 0 )#p.progression()
			i += 1
		if i > 0:
			result = round((result/i),2)
		return result


	def top_entities_percent(self,percent_low,percent_high):
		top_entity = self.top_entity()
		programmes = top_entity.lines()
		result = 0
		for p in programmes:
			if p.progression() <= percent_high and p.progression() >= percent_low:
				result += 1
		return round(result,2)

	def nb_top_entities(self):
		return self.get_entities().first().m_entity_type.lines().count()

	def top_entities_half(self):
		return self.top_entities_percent(25,99)

	def top_entities_full(self):
		return self.top_entities_percent(100,100)

	def top_entities_lower(self):
		return self.top_entities_percent(0,25)

	def earliest_entity(self):
		return self.get_entities().first().m_entity_type.lines().order_by('m_date_modif').first()

	def latest_entity(self):
		return self.get_entities().first().m_entity_type.lines().order_by('m_date_modif').last()

	def operations_modules(self):
		return Aggregate.objects.filter(m_institution__id = self.id).select_related('m_institution').first()

	def operation_defaulted(self):
		return self.default_options

	def operations_name(self):
		name = Aggregate.objects.filter(m_institution__id = self.id).select_related('m_institution').first()
		if name != None and name.m_nom != None:
			name = name.m_nom
		else:
			name = "Opération"
		return name

	def roles(self):
		return Role.objects.filter(actual_institution=self.id)

	class Meta:
		ordering=('nom','sigle',)

class Institution_Periodes(models.Model):
	m_institution = models.ForeignKey(Institution,on_delete = models.CASCADE,blank=True,null=True)
	m_periode = models.ForeignKey(Periode,on_delete = models.CASCADE,blank=True,null=True)
	m_default = models.BooleanField(default=False,blank=True,null=True)
	def __str__(self):
		return str(self.m_periode)

class Structure_Hierachy(models.Model):
	m_institution = models.ForeignKey(Institution,on_delete = models.CASCADE,blank=True,null=True)
	m_levels_fields = models.TextField()# Valeur1|Valeur2
	m_levels_values = models.TextField()# Racine0§Valeur1.1§Valeur..2|
	def get_levels(self):
		fields = self.m_levels_fields.split("|")
		values = self.m_levels_values.split("|")
		n = len(fields)
		result = list()
		for i in range(n-1):
			tmp = dict()
			tmp["field"] = fields[i]
			tmp["values"] = values[i].split("§")
			result.append(tmp)
		return result

	def __str__(self):
		return self.m_levels_fields

class Structure(models.Model):
	photo = models.FileField(blank=True,null=True)
	nom	= models.CharField(max_length=255)
	designation = models.CharField(max_length=255,null=True)
	date_creation = models.DateTimeField(db_index=True,auto_now_add=True)
	institution = models.ForeignKey(Institution,on_delete=models.CASCADE,blank=True,null=True)
	#hierachy = models.ForeignKey(Structure_Hierachy,on_delete=models.CASCADE,blank=True,null=True)
	#values_hierachy = models.TextField(blank=True,null=True)# Valeur1|Valeur2
	parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,related_name='children')
	longitude = models.FloatField(null=True)
	latitude = models.FloatField(null=True)

class GroupeStructure(models.Model):
	nom = models.CharField(null=True,max_length=255)
	structure = models.ManyToManyField(Structure)
	def __str__(self):
		if self.nom != None:
			return self.nom
		else:
			return self.designation

	def struct_hierachy(self):
		values = self.values_hierachy
		if values != None:
			values = values.split("|")[:-1]
		return values

	class Meta:
		ordering=('nom',)

	def taches(self):
		return Tache.objects.filter(structure__id=self.id).select_related('structure')

	def responsable(self):
		return StructureResponsable.objects.filter(m_structure__id=self.id).select_related('m_structure').first().m_responsable

	def nb_taches(self):
		return Tache.objects.filter(structure__id=self.id).select_related('structure').count()

	def progression(self):
		taches = Tache.objects.filter(structure__id=self.id).select_related('structure')
		bool(taches)

		nb_taches = taches.count()
		sommes = 0
		for t in taches:
			sommes += t.progression()
		if nb_taches >0:
			sommes /= nb_taches
		return round(sommes,2)

	def top_entities_percent(self,percent_low,percent_high):
		programmes = self.taches()
		bool(programmes)

		result = 0
		for p in programmes:
			if p.progression() <= percent_high and p.progression() >= percent_low:
				result += 1
		return round(result,2)

	def top_entities_half(self):
		return self.top_entities_percent(25,99)

	def top_entities_full(self):
		return self.top_entities_percent(100,100)

	def top_entities_lower(self):
		return self.top_entities_percent(0,25)
		programmes = top_entity.lines()

class StructureRelation(models.Model):
	m_structure1 = models.ForeignKey(Structure,blank=True,null=True,on_delete=models.SET_NULL,related_name="struc1")
	m_structure2 = models.ForeignKey(Structure,blank=True,null=True,on_delete=models.SET_NULL,related_name="struc2")

class Personnel(models.Model):
	nom	= models.CharField(max_length=128,blank=True,null=True)
	prenom = models.CharField(max_length=128,blank=True,null=True)
	mail = models.CharField(max_length=128,blank=True,null=True)
	tel = models.CharField(max_length=128,blank=True,null=True)
	photo = models.FileField(blank=True,null=True)
	sexe= models.CharField(max_length=255,null=True,blank=True)
	bd_user = models.OneToOneField(User,blank=True,null=True,on_delete=models.CASCADE)
	actual_institution = models.ForeignKey(Institution,blank=True,null=True,on_delete=models.SET_NULL)
	def __str__(self):
		return str(self.photo)
	def backgrounds_tat(self):
		colors = {
				"1":"blue","2":"green","3":"red","4":"blue","5":"blue","6":"blue","7":"blue","8":"blue","9":"blue","0":"blue",
				"a":"orange",
				"b":"green",
				"c":"#350990",
				"d":"#983209","e":"red","f":"brown","g":"purple","h":"cyan","i":"#09a576",
				"j":"#3459b0","k":"#004567","l":"chocolate","m":"brown","n":"#8d53df","o":"darkred",
				"p":"yellowgreen","q":"violet","r":"turquoise","s":"tomato","t":"teal",
				"u":"steelblue","v":"slateblue","w":"peru","x":"orangered","y":"olivedrab","z":"dodgerblue","#":"firebrick"
		}
		return colors[self.initials()[0].lower()]

	def initials(self):
		result = "#"
		if self.nom != None:
			result = self.nom[0]
		if self.prenom != None:
			result += self.prenom[0]
		return result

	def get_taches(self,institution="#"):
		if institution != "#":
			tmp_institution = institution
		else:
			tmp_institution = self.get_institution()
		taches = Operation.objects.filter(personnel__id=self.id).select_related('personnel')
		taches2 = OperationRole.objects.filter(m_personnel__id=self.id).select_related('m_personnel')
		bool(taches)
		bool(taches2)

		result = set()
		for t in taches:
			if institution != "#":
				result.add(t.tache)
			elif t.institution() == tmp_institution:
				result.add(t.tache)

		for t in taches2:
			if "R" in t.role_racis():
				if t.m_operation != None:
					result.add(t.m_operation.tache)

		return result

	def get_operations(self):
		"""
		taches = self.get_taches()
		bool(taches)
		operations = list()
		for t in taches:
			operations += t.operations()
		"""
		operations = Operation.objects.filter(personnel=self.id)
		return operations

	def operations_accounted(self):
		return Operation.objects.filter(accountable=self.id)

	def operations_informed(self):
		taches2 = OperationRole.objects.filter(m_personnel__id=self.id)
		result = set()
		for t in taches2:
			if "I" in t.role_racis():
				if t.m_operation != None:
					result.add(t.m_operation)
		return result


	def get_operations_status(self,nature):
		operations = self.get_operations()
		result = 0
		for o in operations:
			if o.etat == nature:
				result += 1
		return result

	def get_operations_low(self):
		return self.get_operations_status("0")

	def get_operations_medium(self):
		return self.get_operations_status("1")

	def get_operations_high(self):
		return self.get_operations_status("2")

	def raci_roles(self,operation):
		roles = OperationRole.objects.filter(m_operation=operation)
		result = list()
		for r in roles:
			result.append(r)
		return result

	def all_raci_roles(self):
		roles = self.get_operations()# OperationRole.objects.filter(m_personnel__id=self.id)
		result = list()
		for r in roles:
			result.append(r)
		return result

	def progression_taches(self,institution="#"):
		moy = 0
		i = 0
		for t in self.get_taches(institution):
			moy += t.progression()
			i += 1
		if i>0:
			moy /= i
		return round(moy,2)

	def __str__(self):
		result = " "
		if self.prenom != None and self.nom != None:
			result = self.prenom +" "+self.nom
		return result

	def get_function(self,institution=None):
		if institution == None:
			if self.actual_institution != None:
				institution = self.actual_institution.id
		result = Personnel_Function.objects.filter(m_personnel__id=self.id,m_institution__id=institution).first()
		return result

	def get_structure(self,institution=None):
		if institution == None:
			if self.actual_institution != None:
				institution = self.actual_institution.id
		institution = Personnel_Structure.objects.filter(m_personnel__id=self.id,m_structure__institution=institution).first()

		return institution

	def get_institution(self):
		tmp = self.get_structure()
		bool(tmp)
		if tmp != None:
			tmp = self.get_structure().m_structure.institution
		return tmp

	def get_programmes(self):
		result = set()
		permissions = self.get_function(self.actual_institution.id).m_role.permissions
		if permissions > 4:
			taches = Operation.objects.filter(tache__activite__action__programme__institution=self.actual_institution)
		else:
			taches = Operation.objects.filter(personnel__id=self.id,tache__activite__action__programme__institution=self.actual_institution)
		for t in taches:
			result.add(t.tache.activite.action.programme)
		return result
	class Meta:
		ordering=('nom',)

	def all_institutions(self):
		functions = Personnel_Function.objects.filter(m_personnel__id=self.id)
		result = set()
		for f in functions:
			result.add(f.m_institution)
		institutions2 = Institution.objects.filter(owner__m_user=self.bd_user)
		for f in institutions2:
			result.add(f)
		return result#future@gmail.com

	def RACI_entities(self):
		return PersonnelRACI.objects.filter(m_personnel__id=self.id)

	def RACI_list(self):
		tmp = PersonnelRACI.objects.filter(m_personnel__id=self.id)
		result = list()
		for t in tmp:
			result.append(t.m_entity)
		return result

	def RACI_manage(self):
		entity = self.RACI_entities()
		a = entity.first()
		if a == None:
			tmp = [None,None]
		else:
			tmp = [a.m_entity,a.m_roles]
		return tmp

class Personnel_Structure(models.Model):
	m_personnel = models.ForeignKey(Personnel,blank=True,null=True,on_delete=models.CASCADE)
	m_structure = models.ForeignKey(Structure,blank=True,null=True,on_delete=models.CASCADE)
	m_start_date = models.DateTimeField(db_index=True,auto_now_add=True)
	m_responsable = models.BooleanField(default=False,blank=True,null=True)
	def __str__(self):
		return str(self.m_structure)
	class Meta:
		ordering=('-m_structure__institution','-m_start_date','m_structure',)

class StructureResponsable(models.Model):
	m_structure = models.ForeignKey(Structure,blank=True,null=True,on_delete=models.CASCADE)
	m_responsable = models.ForeignKey(Personnel,blank=True,null=True,on_delete=models.CASCADE)
	m_date_start = models.DateTimeField(db_index=True,auto_now_add=True)
	m_date_end = models.DateTimeField(blank=True,null=True)
	class Meta:
		ordering=('m_structure','-m_date_start',)

class EntityType(models.Model):
	m_nom = models.CharField(max_length=128,blank=True,null=True)
	m_date_creation = models.DateTimeField(db_index=True,auto_now_add=True)
	m_date_modif = models.DateTimeField(auto_now=True)
	# Expected Fields
	m_fields = models.TextField(default="",blank=True,null=True)
	m_type_fields = models.TextField(default="",blank=True,null=True)
	# Fields for Rapport
	m_fields_rapported = models.TextField(default="",blank=True,null=True)
	m_type_fields_rapp = models.TextField(default="",blank=True,null=True)
	# Entity for Taches
	m_fields_calculate = models.TextField(default="",blank=True,null=True)
	m_fields_fonction_calculate = models.TextField(default="",blank=True,null=True)
	#fonction 1|nb_fields|function

	# For List Values
	m_enum_values = models.TextField(default="",blank=True,null=True)

	is_pic_represented = models.BooleanField(default=False,blank=True,null=True)
	is_tache = models.BooleanField(default=False,blank=True,null=True)

	indicateur_fields = models.TextField(default="",blank=True,null=True)
	m_indicateurs_values = models.TextField(blank=True,null=True)
	def __str__(self):
		return str(self.m_nom)

	def nb_indicateurs_accomplshed(self):
		result = 0
		tmp = self.get_indicateurs()
		for t in tmp:
			i = IndicateurValue.objects.filter(m_indicateur__id=self.id).first()
			if i != None:
				result += 1

		total = tmp.count()
		if total > 0:
			percent = round((result * 100 / total),2)
		else:
			percent = 0
		class Datas:
			nb = None
			total = None
			percent = None
		data = Datas()
		data.nb = result
		data.total = total
		data.percent = percent
		return data

	def hierachie(self):
		ins = InsitutionEntities.objects.filter(m_entity_type__id=self.id).first()
		if ins == None:
			result = None
		else:
			result = ins.m_hierachie
		return result

	def absolute_hierachie(self):
		ins = InsitutionEntities.objects.filter(m_entity_type__id=self.id).first()
		ins0 = ins.m_institution
		all_ins  = InsitutionEntities.objects.filter(m_institution=ins0).count()
		if ins == None:
			result = None
		else:
			result = all_ins - ins.m_hierachie
		return result

	def sup_entity(self,arg_institution):
		result = None
		institution = Institution.objects.get(id=arg_institution)

		bool(institution)
		ies = InsitutionEntities.objects.filter(m_institution=institution,m_entity_type__id=self.id).select_related('m_entity_type').first()
		bool(ies)

		if ies != None:
			hierachie = ies.m_hierachie
			if hierachie > 0:
				tmp_hierachie = hierachie - 1
				result = InsitutionEntities.objects.filter(m_institution=institution,m_hierachie = tmp_hierachie).select_related('m_institution').first()
				bool(result)
				if result != None:
					result = result.m_entity_type
		return result

	def fields(self):
		fields = self.m_fields.split("|")[:-1]
		return fields

	def type_fields(self):
		fields = self.m_type_fields.split("|")[:-1]
		return fields

	def fields_rapported(self):
		if self.m_fields_rapported != None:
			fields = self.m_fields_rapported.split("|")[:-1]
		else:
			fields = list()
		return fields

	def type_fields_rapported(self):
		fields = self.m_type_fields_rapp.split("|")[:-1]
		return fields

	def lines(self):
		if self.is_tache:
			results = Tache.objects.filter(m_type_entity__id=self.id).select_related('m_type_entity')
		else:
			results = Entity.objects.filter(m_type_entity__id=self.id).select_related('m_type_entity')
		return results

	def objects_field(self):
		results = list()
		index = 0
		for f in self.fields():
			results.append({'label':f})
		for f in self.type_fields():
			results[index]['type'] = f
			index += 1
		return results

	def calculates_field(self):
		result = list()
		for field in self.m_fields_calculate.split('|')[:-1]:
			result.append(int(field))
		return result

	def get_calculate_funct(self):
		functions = self.m_fields_fonction_calculate.split('\n')
		result = dict()
		for f in functions:
			tmp_func = f.split('|')
			result[tmp_func[0]] = tmp_func[1]
		return result

	def enum_values(self):
		result = dict()
		lines = self.m_enum_values.split("\n")
		for l in lines[:-1] :
			result[l.split("#")[0]] = l.split("#")[1].split("|")[:-1]
		return result

	def enum_fields(self):
		fields = self.type_fields()
		result = list()
		i =0
		for f in fields:
			if f == 'enum':
				nm = self.fields()[i]
				try:
					tmp = {
						'name':nm,
						'lines':self.enum_values()[nm]
					}
				except:
					tmp = {
						'name':nm,
						'lines':list()
					}
				result.append(tmp)
			i+=1
		return {'nb':i,'result':result}

	def get_institution(self,institution=None):
		if institution != None:
			iS = InsitutionEntities.objects.filter(m_institution=institution,m_entity_type__id=self.id).first()
		else:
			iS = InsitutionEntities.objects.filter(m_entity_type__id=self.id).first()
		if iS != None:
			iS = iS.m_institution
		return iS

	def indicateurs(self,spo=True):
		result = list()
		tmp = self.indicateur_fields.split("\n")
		if not spo:
			for t in tmp:
				result.append(t.split("|"))
		else:
			for t in tmp:
				a2 = t.split("|")
				try:
					b2 = {
					"label":a2[0],
					"type":a2[1]
					}
					result.append(b2)
				except:
					pass
		return result

class Entity(models.Model):
	m_nom = models.CharField(max_length=256,blank=True,null=True)
	m_date_creation = models.DateTimeField(db_index=True,auto_now_add=True)
	m_date_modif = models.DateTimeField(auto_now=True)
	m_type_entity = models.ForeignKey(EntityType,blank=True,null=True,on_delete=models.CASCADE)
	m_value_fields = models.TextField(blank=True,null=True)
	is_rapported = models.BooleanField(default=False,blank=True,null=True)
	m_reported_fields = models.TextField(blank=True,null=True)

	m_pic_represented = models.FileField(blank=True,null=True)
	m_indicateurs_reels = models.TextField(blank=True,null=True)
	dataset = models.ManyToManyField('DataSet', blank=True)
	def __str__(self):
		return self.m_nom or "Unnamed Entity"  


	def sup_hierachie(self):
		tmp = self.sup_entity()
		tmp2 = tmp
		result = list()
		da_verse = list()
		while tmp != None:
			result.append(tmp)
			tmp = tmp.sup_entity()

		return reversed(result)

	def get_objectif(self):
		index = self.search_value("Objectif")
		result = None
		if index != -1:
			tmp = self.values() + self.values_repport()
			try:
				result = tmp[index]
			except:
				result = None
		if result is not None:
			result = ' - '.join(result.splitlines())
		return result

	def search_value(self,value):
		i = 0
		find = False
		try:
			fields = self.m_type_entity.fields() + self.m_type_entity.fields_rapported()
		except:
			fields = list()
		for f in fields :
			if value in f:
				find = True
				break
			else:
				i+=1
		if not find:
			i = -1
		return i

	def get_indicateurs(self):
		result = Indicateur.objects.filter(m_enti__id=self.id)
		return result

	def get_indicateurs_values(self):
		result = IndicateurValue.objects.filter(m_entity__id=self.id)
		return result

	def top_entities_percent(self,percent_low,percent_high):
		subs = self.sub_entities()
		programmes = self.sub_entities()
		result = 0
		for p in programmes:
			if p.progression() <= percent_high and p.progression() >= percent_low:
				result += 1
		return result

	def top_entities_half(self):
		return self.top_entities_percent(25,99)

	def top_entities_full(self):
		return self.top_entities_percent(100,100)

	def top_entities_lower(self):
		return self.top_entities_percent(0,25)

	def force_delete(self):
		if self.m_type_entity.is_tache == True:
			self.delete()
		else:
			sub_entities = self.sub_entities()
			hierachies = EntityHierachie.objects.filter(m_sub_entity__id=self.id)
			hierachies.delete()
			if sub_entities == set():
				self.delete()

	def child_trees(self):
		t = self.m_type_entity.is_tache
		subs = self.sub_entities()
		resul = [subs]
		while t != True and subs != list():
			if subs != list():
				t = subs[0].m_type_entity.is_tache
				subs = subs[0].sub_entities()
			else:
				t = True
			resul.append(subs)
		return resul

	def levels(self,lvl,institution):
		if lvl != -1:
			hierachie = InsitutionEntities.objects.filter(m_institution=institution,m_entity_type=self.m_type_entity).first().m_hierachie
			diff_hierachie = lvl - hierachie
			res = [Entity.objects.get(id=self.id)]
			for i in range(diff_hierachie):
				tmp = list()
				for r in res:
					tmp+=r.sub_entities()
				res = tmp
		else:
			res = [self.taches()]
		return res

	def taches(self):
		results = set()
		if self.m_type_entity.is_tache == False:
			ops = self.operations()
			for o in ops:
				results.add(o.tache)
		return results

	def operations(self):
		hierachie = self.m_type_entity.hierachie()
		ops = Operation.objects.filter()
		result = list()
		for o in ops:
			try:
				if o.code.split("#")[hierachie] == str(self.id):
					result.append(o)
			except:
				pass
		return result

	def __str__(self):
		return str(self.m_type_entity) + ' : '+str(self.get_name())

	def get_name(self):
		code = self.get_value("Code ")
		if code == None:
			result = ""
		else:
			result = code + " - "

		if self.values() != list():
			s = result + ' - '.join(self.values()[0].splitlines())
		else:
			s = result
		return s

	def get_name_no_under(self):
		result = ""
		if self.values() != list():
			result = str(self.values()[0].split("\n"))
		return result



	def values(self):
		try:
			tmp = self.m_value_fields.split("|")[:-1]
			type_fields = self.m_type_entity.type_fields()
		except:
			type_fields = list()
		i=0

		for t in type_fields:
			try:
				if t == 'file':
					if tmp[i] not in ['',' ']:
						elt = EntityFile.objects.get(id=int(tmp[i]))
						tmp[i] = "<i class='fas fa-file'></i> <a href='"+elt.m_file.url+"'>" + str(elt) + "</a>"
				elif t == 'image':
					if tmp[i] not in ['',' ']:
						elt = EntityFile.objects.get(id=int(tmp[i]))
						tmp[i] = "<img style='border-radius:10%;width:40px;height:40px;' src='"+elt.m_file.url+"' >"
				i+=1
			except:
				pass

		if self.m_type_entity != None:
			for t in self.m_type_entity.calculates_field():
				functi = self.m_type_entity.get_calculate_funct()[str(t)]
				for i in range(t):
					functi = functi.replace("A"+str(i),"int(tmp["+str(i)+"])")
				tmp[(t-1)] = eval(functi)
		return tmp

	def get_value(self,value):
		index = self.search_value(value)
		if index != -1:
			result = self.values()[index]
		else:
			result = None
		return result

	def set_value(self,value,b):
		index = self.search_value(value)
		if index != -1:
			values = self.values()
		else:
			values = list()
		if index != -1:
			try:
				values[index] = b
			except:
				pass
		# save encore en proto
		tmp = "|".join(values)+"|"
		self.m_value_fields = tmp

	def set_name(self,nom):
		values = self.values()
		tmp = ""
		values[0] = nom

		for v in values:
			tmp += str(v) + "|"
		self.m_value_fields = tmp

	def global_values(self):
		fields = self.m_type_entity.fields()
		values = self.values()
		i=0
		result = list()
		try:
			for v in values:
				result.append({'name':fields[i],'value':v})
				i+=1
		except:
			pass
		if self.m_type_entity.is_tache and self.m_type_entity.get_institution().finan_options == True:
			result.append({'name':"montant Allloue","value":Tache.objects.get(id=int(self.id).montant)})
		return result

	def values_repport(self):
		if self.m_reported_fields != None:
			result = self.m_reported_fields.split("|")[:-1]
		else:
			result = list()
		return result

	def tache(self):
		return Tache.objects.filter(id=self.id).first()

	def progression(self):  
		result = 0  
		hierachie = self.m_type_entity.hierachie()  

		if self.m_type_entity.is_tache:  
			tache = Tache.objects.get(id=self.id)  
			result = tache.progression()  
		else:  
			operations = Operation.objects.filter().values('etat', 'code')  
			i = 0  
			for o in operations:  
				try:  
					lvls = o['code'].split("#")  
					if hierachie < len(lvls) and lvls[hierachie] == str(self.id):  
						result += (100 if o['etat'] == '2' else 0)  
						i += 1  
				except Exception as e:  
					pass
			if i > 0:  
				result /= i  

		return round(result, 2)	

	def technical_progression(self):
		indicateurs = Indicateur.objects.filter(m_enti__id=self.id)
		actual_year = datetime.now().year
		nb_good = 0
		nb_indic = 0
		result = 0
		for indi in indicateurs:
			cible = indi.get_cibles(actual_year)
			valeur = indi.actu_value(actual_year)
			if float(valeur) >= float(cible):
				nb_good += 1
			nb_indic += 1
		if nb_indic > 0:
			result = 100*nb_good/nb_indic
		return result

	def finan_progression(self):
		operations = self.operations()
		tmp = 0
		tmp2 = 0
		if self.m_type_entity.is_tache == False:
			taches = self.taches()
		else:
			taches = [Tache.objects.get(id=e.id)]
			for t in taches:
				if t.montant != None:
					tmp += t.montant
			for o in operations:
				tmp2 += o.montant2
		if tmp > 0:
			result = 100*tmp2/tmp
		else:
			result = 0
		return result

	def sub_entities(self):
		result = list()
		if self.m_type_entity.is_tache == True:
			result = Operation.objects.filter(tache__id=self.id).select_related('tache')
		else:
			relations = EntityHierachie.objects.filter(m_sup_entity__id = self.id).select_related('m_sup_entity')
			bool(relations)
			test = None
			try:
				test = relations[0].m_type_entity.is_tache
			except:
				pass
			for r in relations:#
				r2 = r.m_sub_entity
				if r2 is not None:
					try:
						if r2.m_type_entity.is_tache:
							result.append(Tache.objects.get(id=r2.id))
						else:
							result.append(r.m_sub_entity)
						"""
						if r.m_sub_entity.m_type_entity.is_tache != True:
							result.add(r.m_sub_entity)
						else:
							result.add(Tache.objects.get(id=r.m_sub_entity.id))
						"""
					except:
						pass
		return result

	def name_sub(self):
		elt = EntityHierachie.objects.filter(m_sup_entity__id = self.id).first()
		if elt != None:
			elt = elt.m_sub_entity.m_type_entity
		return elt

	def nb_sub(self):
		return EntityHierachie.objects.filter(m_sup_entity__id = self.id).count()

	def sup_entity(self):
		tmp = EntityHierachie.objects.filter(m_sub_entity__id=self.id).first()
		if tmp != None :
			tmp = tmp.m_sup_entity
		return tmp

	def rapport(self):
		pass

	def structure(self):
		return Tache.objects.get(id=self.id).structure

	def personnelRACI(self):
		pR = PersonnelRACI.objects.filter(m_entity__id=self.id)
		res = {
			"personnels":list(),
			"responsable":[None],
			"accounted":[None],
			"consulted":[None],
			"informed":[None]
		}
		for p in pR:
			perso = p.m_personnel
			res["personnels"].append(perso)
			roles = p.m_roles.split("|")
			if roles[0] == "1":
				res["responsable"].append(perso)
			if roles[1] == "1":
				res["accounted"].append(perso)
			if roles[2] == "1":
				res["consulted"].append(perso)
			if roles[3] == "1":
				res["informed"].append(perso)
		return res

	class Meta:
		ordering=('m_type_entity','m_value_fields',)


class Role(models.Model):
	nom = models.CharField(max_length=64,blank=True,null=True)
	description = models.TextField(blank=True,null=True)
	actual_institution = models.ForeignKey(Institution,on_delete = models.CASCADE,blank=True,null=True)
	permissions = models.IntegerField(default=0,blank=True,null=True)
	#supervisor_roles
	m_nature = models.CharField(max_length=2,default="0",blank=True,null=True)
	#user_simple
	is_simple_user = models.IntegerField(default=0,blank=True,null=True)
	m_simple_auth = models.ForeignKey(EntityType,on_delete = models.CASCADE,blank=True,null=True)
	#entities_user

	m_extra_fields = models.TextField(default="",blank=True,null=True)
	m_extra_types = models.TextField(default="",blank=True,null=True)

	def get_fields1(self):
		j = 0
		extra_fields = self.m_extra_fields.split("|")
		extra_types = self.m_extra_types.split("|")
		n = len(extra_types)
		result = list()
		for i in range(j,n):
			try:
				result.append({"field":extra_fields[i],"type":extra_types[i]})
			except:
				pass
		return result

	def __str__(self):
		return self.nom

	def entity_levels(self):
		result =list()
		if self.m_simple_auth != None:
			hierachie = self.m_simple_auth.hierachie()
			if hierachie == 0:
				result = list(self.actual_institution.get_entities())[0]
				result = [result]
			else:
				result = list(self.actual_institution.get_entities())[:hierachie]
			#result = [hierachie]
		return result

	def permission(self):
		entities = self.actual_institution.get_entities()
		bool(entities)
		last_entity = entities.last().m_entity_type
		hierachies = entities.last().m_hierachie+1

		if self.permissions == 0:
			result = "Opérant : Execute et Fait un Rapport sur l'Evolution : "+str(last_entity)
		elif self.permissions > hierachies:
			result = "Manager : Administre la Plateforme"
		elif self.permissions < 0:
			result = None
		else:
			tmp_hierachie = int(hierachies - self.permissions)
			institution = entities.filter(m_hierachie=tmp_hierachie).first()
			result = " Chargé "+str(institution)+" : Supervise l'Evolution "+str(institution)
		return result

	def persos(self):
		return Personnel_Function.objects.filter(m_role__id=self.id)


class Personnel_Function(models.Model):
	m_personnel = models.ForeignKey(Personnel,blank=True,null=True,on_delete=models.CASCADE)
	m_role = models.ForeignKey(Role,blank=True,null=True,on_delete=models.CASCADE)
	m_start_date = models.DateTimeField(db_index=True,auto_now_add=True)
	m_institution = models.ForeignKey(Institution,blank=True,null=True,on_delete=models.CASCADE)
	# Entity concerned
	m_entity = models.ForeignKey(Entity,blank=True,null=True,on_delete=models.CASCADE)
	m_extra_values = models.TextField(blank=True,null=True)
	def __str__(self):
		return str(self.m_role)

	def get_values1(self):
		fields1 = self.m_role.get_fields1()
		if self.m_extra_values != None:
			values = self.m_extra_values.split("|")
		else:
			values = list()
		n = len(values)
		result = list()
		for i in range(0,n):
			try:
				if fields1[i]["type"] == "file":
					tmp = Personnel_File.objects.get(id=int(values[i]))
					if tmp != None:
						tmp = "<a href='"+tmp.m_file.url+"'><i class='fas fa-file'></i> "+tmp.m_name+"</a> "
					result.append(tmp)
				else:
					result.append(values[i])
			except:
				pass
		return result

	def get_values2(self):
		fields = self.m_role.get_fields1()
		values = self.get_values1()
		result = list()
		n = len(values)
		for i in range(0,n):
			result.append({"val":values[i],"field":fields[i]})
		return result

	class Meta:
		ordering=('-m_start_date',)


class Personnel_File(models.Model):
	m_file = models.FileField(blank=True,null=True)
	m_name = models.TextField(blank=True,null=True)

class DataElement(models.Model):
	m_logo = models.FileField(blank=True,null=True)
	m_name = models.CharField(max_length=255, blank=True, null=True, default='255')
	m_fields_type = models.TextField(blank=True,null=True)
	m_fields = models.TextField(blank=True,null=True)
	m_description = models.TextField(blank=True,null=True)

	m_domain_type = models.CharField(max_length=64,blank=True,null=True,default="Aggregate")
	m_value_type = models.CharField(max_length=64,blank=True,null=True,default="Number")
	m_aggregation_type = models.CharField(max_length=64,blank=True,null=True,default="A")

	is_zero_collect  = models.BooleanField(blank=True,null=True)
	m_default_value = models.IntegerField(blank=True,null=True)
	m_institution = models.ForeignKey(Institution,blank=True,null=True,on_delete=models.CASCADE)

	is_constant =  models.BooleanField(blank=True,null=True)
	nicename = models.CharField(null=True,max_length=255)


	def __str__(self):
		return str(self.m_name)

	def element_values(self,structure=None,dataset=None):
		results = DSet_DElt.objects.filter(m_dataelement__id=self.id)
		if dataset != None:
			results = results.filter(m_dataset_value__m_dataset = dataset)
		if structure != None:
			results = results.filter(m_dataset_value__m_structures=structure )
		return results

	def period_values(self,arg_dataset=None):
		class DEL:
			def __init__(self,e1,e2,e3=0):
				self.sup_period = e1
				self.period = e2
				self.value = e3
			def __repr__(self):
				return str(self.sup_period) + str(self.value)

		tmps = self.element_values(None,arg_dataset)
		periods_tmp = dict()
		p_tmps = list()

		for t in tmps:
			a = t.m_dataset_value.m_period_value+"-"+t.m_dataset_value.m_sub_period_value
			if a in	p_tmps:
				if t.m_value not in ["",None]:
					periods_tmp[a].value += int(t.m_value)
			else:
				elts = DEL(t.m_dataset_value.m_sub_period_value,t.m_dataset_value.m_period_value,0)
				if t.m_value not in ["",None]:
					elts.value = int(t.m_value)
				else:
					elts.value = 0
				periods_tmp[a] = elts
				p_tmps.append(a)

		return (p_tmps,periods_tmp)

	def values_values(self,period="#",dataset=None):
		tmp = self.period_values(dataset)
		result = dict()
		for t in tmp[0]:
			result[t] = tmp[1][t].value
		if period != "#":
			if period in tmp[0]:
				result = result[period]
			else:
				result = 0
		return result

	def fields_group(self):
		tmp = list()
		i = 0
		for f in self.m_fields:
			t = dict()
			t['field'] = m_fields_type[i]
			t['value'] = f
			tmp.append(t)
			i+=1
		return tmp


	class Meta:
		ordering=('m_name',)
# class NatureIndicateur(models.Model):
# 	libelle = models.CharField(null=True,max_length=255)
class GroupeElement(models.Model):
	nom = models.CharField(null=True,max_length=255)
	element = models.ManyToManyField(DataElement)


class Indicateur(models.Model):
	# groupe_indicateur = models.ManyToManyField(GroupeIndicateur)
	#master_indicateur = models.ForeignKey(MasterIndicateur,null=True,blank=True,on_delete=models.CASCADE)
	type_aggregation = models.CharField(max_length=255,null=True)
	# natureindicateur = models.ForeignKey(NatureIndicateur,on_delete=models.CASCADE,null=True)
	m_name = models.CharField(max_length=255,null=True)
	# Periode de Ciblage et de Suivi
	m_periodicite = models.TextField(blank=True,null=True)
	m_sub_periodicite = models.TextField(blank=True,null=True)

	m_final_cible = models.TextField(blank=True,null=True)
	m_cibles = models.TextField(blank=True,null=True)
	m_sources_data = models.TextField(blank=True,null=True)

	m_data_verification = models.TextField(blank=True,null=True)
	m_objectif_indi = models.TextField(blank=True,null=True,default='true')
	m_verification_indi =  models.CharField(max_length=10000,blank=True,null=True) #Moyen | Valeur

	#m_sources_mesures = DataSet
	m_colors_code = models.CharField(max_length=128,blank=True,null=True)#vala|valb|color$
	m_alerts_code= models.CharField(max_length=128,blank=True,null=True)#inf#sup#calert$
	m_fields = models.TextField(blank=True,null=True)#autres
	m_others = models.TextField(blank=True,null=True)#autres
	m_enti = models.ForeignKey(Entity,blank=True,null=True,on_delete=models.CASCADE)
	m_institution = models.ForeignKey(Institution,blank=True,null=True,on_delete=models.CASCADE)

	#new champs
	m_numerateur = models.CharField(max_length=10000,blank=True,null=True)
	m_denominateur = models.CharField(max_length=10000,blank=True,null=True)
	m_unite = models.CharField(max_length=255,default='%',blank=True,null=True)
	m_coefficient = models.IntegerField(blank=True,null=True)
	m_fields = models.TextField(blank=True,null=True)#autres

	m_values = models.TextField(blank=True,null=True)
	m_datalets_calcul = models.CharField(max_length=10000,blank=True,null=True)
	m_start_date = models.DateTimeField(db_index=True,blank=True,null=True,auto_now_add=True)

	m_secundo_options = models.TextField(blank=True,null=True)
	nicename = models.CharField(max_length=255,null=True)
	def __str__(self):
		return self.m_name

	class Meta:
		ordering=('-m_start_date',)

	def get_colors_elts(self):
		colors = list()
		if self.m_colors_code != None:
			colors = self.m_colors_code.split("$")
		return colors

	def data_verification(self):
		verifications = self.m_data_verification.split("#")
		if verifications[0] == "1" and len(verifications) > 1:
			result = DataSet.objects.get(id=verifications[1])
		else:
			result = None
		return result

	def get_alerts_code(self):
		alerts = list()
		if self.m_alerts_code != None:
			alerts = self.m_alerts_code.split("$")
		return alerts

	def indicateur_values(self):
		return IndicateurVal.objects.filter(m_indicateur__id = self.id)

	def period_values(self,no_join=True):
		elemts = self.indi_numerateur()
		periods = list()
		for e in elemts:
			tmp = e.period_values()[0]
			for t in tmp:
				if t not in periods:
					periods.append(t)
		result = periods
		if no_join:
			result = "#".join(result)
		return result

	def period_elements(self):
		period = self.period_values(False)
		elemts = self.indi_numerateur()
		result = list()
		tmp_result = dict()
		variables = dict()
		for p in period:
			for e in elemts:
				tmp_pV = e.period_values()
				if p in tmp_pV[0] and tmp_pV[1][p].value != None:
					tmp =tmp_pV[1][p].value
				else:
					tmp = 0
				#result.append(tmp)
				variables[str(e.id)+"#"+str(p)] = tmp

		return variables

	def value_numerateur(self):
		tmp = self.m_numerateur
		tmp = tmp.split("$")
		result = list()
		for t in tmp:
			try:
				result.append(DataElement.objects.get(id=int(t)))
			except:
				pass
		return result

	def value_denum(self):
		tmp = self.m_denominateur
		tmp = tmp.split("$")
		result = list()
		for t in tmp:
			try:
				result.append(DataElement.objects.get(id=int(t)))
			except:
				pass
		return result

	def indi_numerateur(self):
		"""
		try:
			indicateur = DataElement.objects.filter(id=int(self.m_numerateur))
		except:
			indicateur = DataElement.objects.filter(m_name = self.m_numerateur)
		if indicateur != None:
			indicateur = indicateur.first()
		"""
		indicateur = self.value_numerateur()
		return indicateur

	def indi_denum(self):
		"""
		try:
			indicateur = DataElement.objects.filter(id=int(self.m_denominateur))
		except:
			indicateur = DataElement.objects.filter(m_name = self.m_denominateur)
		if indicateur != None:
			indicateur = indicateur.first()
		"""
		indicateur = self.value_denum()
		return indicateur

	def values_split(self):
		return self.m_values.split("\n")

	def first_values(
	self):
		return self.values_split()[0]

	def period_last(self):
		tmp = self.first_values()
		result = tmp.split("#")
		return result[0]

	def value_last(self):
		tmp = self.first_values()
		result = tmp.split("#")
		return str(result[1]) + " sur " + str(self.m_denominateur.split("#")[1])

	def indivals(self):
		return IndicateurVal.objects.filter(m_indicateur__id=self.id)

	def get_cibles(self, actual_year):
		cibles = self.m_cibles
		cib = cibles.split("$")
		result = 0
		for ci in cib:
			c = ci.split("#")
			if len(c) > 1:
				b = c[1].split("|")
				if b[0] == str(actual_year):
					result = b[1]
					break
					return result

	def actu_value(self,period="#"):
		iV = IndicateurVal.objects.filter(m_indicateur__id=self.id)
		data_verification = self.data_verification()
		formula = self.m_numerateur + "*" +str(self.m_coefficient)
		if self.m_denominateur not in [None,""]:
			formula += "/" +self.m_denominateur
		formula = formula.lower()
		if period == "#":
			periodes = self.period_values(False)
		else:
			periodes = [period]
		def evaluate(expression,indicateurs=iV,period="#"):

			def avg(elts):
				if len(elts) > 0:
					return sum(elts)/len(elts)
				else:
					return 0

			def product(elts):
				result = 1
				for e in elts:
					result *= e
				return result

			def variance(elts):
				s = 0
				for e in elts:
					s += e*e
				return s - avg(elts)*avg(elts)

			def e_type(elts):
				return sqrt(variance(elts))

			def is_null(elts):
				result = True
				for e in elts:
					if e != None:
						result = False
						break
				return result
			# ex : mean($1$) + max($2$)
			# get variables

			tmp = ""
			list_var = list()
			is_v = 0
			expression = expression.replace("($","([$")
			expression = expression.replace("$)","$])")
			for e in expression:
				if e != '$' and is_v == 1:
					tmp += e
				elif e == '$' and is_v == 0:
					is_v = 1
				elif e == '$' and is_v == 1:
					if tmp != "":
						list_var.append(tmp)
					tmp = ""
					is_v = 0
			#replace
			#return periodes
			result = list()

			for p in periodes:
				expression2 = expression
				for c in list_var:
					element = DataElement.objects.get(id=int(c))
					value = element.values_values(p,data_verification)
					expression2 = expression2.replace("$"+str(c)+"$",str(value))
				try:
					tmp = eval(expression2)
					result.append(tmp)
				except:
					result.append(-1)#expression2
			return result

		if iV != None:
			pass#iV =iV.value_calcul()
		else:
			pass
		return evaluate(formula)

	def last_value(self):
		try:
			result = self.actu_value()[-1]
		except:
			result = None
		try:
			result = result[0]
		except:
			pass
		return result
class GroupeIndicateur(models.Model):
	libelle = models.CharField(null=True,max_length=255)
	indicateur = models.ManyToManyField(Indicateur)
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# # Définition du signal post-save en dehors du corps de la classe du modèle
# @receiver(post_save, sender=Indicateur)
# def save_last_value_with_indicateur(sender, instance, created, **kwargs):
# 	if created:
# 		result = instance.last_value()  # Appel de la méthode last_value pour obtenir la valeur
# 		indicateur_associé = instance.indicateur  # Supposons que vous ayez un champ indiquant l'indicateur associé à DataSetValue
# 		IndicateurValeur.objects.create(indicateur_id=indicateur_associé, dataset_value=instance, valeur=result)
#



	def dataset(self):
		return DataSet.objects.filter(m_indicateur__id=self.id).last()


class DataSet(models.Model):
	"""docstring for DataSet"""
	m_name = models.CharField(max_length=64,blank=True,null=True)

	m_indicateur = models.ForeignKey(Indicateur,blank=True,null=True,on_delete=models.CASCADE)	#Detacher INDICAT

	m_institution = models.ForeignKey(Institution,blank=True,null=True,on_delete=models.CASCADE)	#Detacher INDICAT
	m_dataelements = models.ManyToManyField(DataElement)
	m_indicateurs = models.ManyToManyField(Indicateur,related_name="indicateurs")
	m_structures = models.ManyToManyField(Structure)
	m_roles = models.ManyToManyField(Role)

	periodicite = models.ForeignKey(Periode,blank=True,null=True,on_delete=models.CASCADE)
	m_sub_periode = models.CharField(max_length=64,blank=True,null=True)

	m_formulaire = models.TextField(blank=True,null=True)
	#m_periodes
	m_start_date = models.DateTimeField(db_index=True,blank=True,null=True,auto_now_add=True)
	# double_check = models.BooleanField(default=False)
	# files = models.FileField(null=True)

	def join_structures(self):
		structures = self.m_structures.filter()
		result = ""
		for s in structures:
			result += str(s.id) + "#"
		return result

	def join_roles(self):
		roles = self.m_roles.filter()
		result = ""
		for s in roles:
			result += str(s.id) + "#"
		return result

	def join_dataelts(self):
		datasets= self.m_dataelements.filter()
		result = ""
		for s in datasets:
			result += str(s.id) + "#"
		return result

	def join_indicateurs(self):
		datasets= self.m_indicateurs.filter()
		result = ""
		for s in datasets:
			result += str(s.id) + "#"
		return result

	def period(self):
		result = None
		annees = ["Annuelle","Mensuelle","Hebdomadaire"]
		if self.m_periode is not None:
			result =annees[int(self.m_periode)]
		return result

	def __str__(self):
		result = "Formulaire de Donnees : "+str(self.id)
		if self.m_name != None :
			result = self.m_name
		return result

	class Meta:
		ordering=('-m_start_date',)

	def dS_values(self):
		return DataSetValue.objects.filter(m_dataset__id=self.id)

class DataSetValue(models.Model):
	m_dataset = models.ForeignKey(DataSet,blank=True,null=True,on_delete=models.CASCADE)
	m_date_creation = models.DateTimeField(db_index=True,blank=True,null=True,auto_now_add=True)
	m_user = models.ForeignKey(Personnel,blank=True,null=True,on_delete=models.CASCADE)
	m_period_value = models.CharField(max_length=128,blank=True,null=True)
	m_sub_period_value = models.CharField(max_length=128,blank=True,null=True)
	m_structures = models.ManyToManyField(Structure)
	def elt_values(self):
		return DSet_DElt.objects.filter(m_dataset_value__id=self.id)

	class Meta:
		ordering=('-m_date_creation',)



class PeriodeOk(models.Model):
		nom = models.CharField(null=True,blank=True,max_length=255)
		periodicite = models.ForeignKey(Periode,on_delete=models.CASCADE,null=True,blank=True)
		annee = models.IntegerField(null=True,blank=True)
		numero_ordre = models.IntegerField(null=True,blank=True)
		# history = AuditlogHistoryField()
		institution = models.ForeignKey(Institution,on_delete=models.CASCADE,null=True,blank=True)
		nicename = models.CharField(null=True,max_length=255)





class DSet_DElt(models.Model):
	m_dataset_value = models.ForeignKey(DataSetValue,blank=True,null=True,on_delete=models.CASCADE)
	m_dataelement = models.ForeignKey(DataElement,blank=True,null=True,on_delete=models.CASCADE)
	m_structure = models.ForeignKey(Structure,blank=True,null=True,on_delete=models.CASCADE)
	periode=models.ForeignKey(PeriodeOk,null=True,blank=True,on_delete=models.CASCADE)
	m_value= models.IntegerField(blank=True,null=True)
	date_saisie = models.DateField(null=True)
	date_element = models.DateField(null=True)
	texte_element = models.TextField(null=True)
	






class DataSetEntity(models.Model):
	m_dataset = models.ForeignKey(DataSet,blank=True,null=True,on_delete=models.CASCADE)
	m_entity = models.ForeignKey(Entity,blank=True,null=True,on_delete=models.CASCADE)

class DataSetEntityType(models.Model):
	m_dataset = models.ForeignKey(DataSet,blank=True,null=True,on_delete=models.CASCADE)
	m_entity = models.ForeignKey(EntityType,blank=True,null=True,on_delete=models.CASCADE)

class IndicateurPeriode(models.Model):
	m_periode = models.CharField(max_length=128,blank=True,null=True)
	m_sub_periode = models.CharField(max_length=128,blank=True,null=True)
	m_type = models.CharField(max_length=128,blank=True,null=True)
	def __str__(self):
		return str(self.m_periode) + " - "+str(self.m_sub_periode)


class EntityFile(models.Model):
	m_entity = models.ForeignKey(Entity,on_delete=models.SET_NULL,blank=True,null=True)
	m_field = models.CharField(max_length=32,blank=True,null=True)
	m_file = models.FileField(blank=True,null=True)
	def __str__(self):
		return str(self.m_file)

class EntityHierachie(models.Model):#PROTECT
	m_sup_entity = models.ForeignKey(Entity,on_delete=models.CASCADE,blank=True,related_name='sup',null=True)
	m_sub_entity = models.ForeignKey(Entity,on_delete=models.CASCADE,default=None,blank=True,related_name='sub_entity',null=True)
	def sub_tache(self):
		return Tache.objects.filter(id=self.m_sub_entity.id).first()
	def __str__(self):
		return str(self.m_sup_entity) + " --> "+str(self.m_sub_entity)
	class Meta:
		ordering=('m_sup_entity','m_sub_entity',)

class StructureRole(models.Model):
	m_structure = models.ForeignKey(Structure,on_delete=models.CASCADE,blank=True,null=True)
	m_role = models.TextField(blank=True,null=True)
	def __str__(self):
		return str(self.m_structure) + "  " + self.m_role

	def short_role(self):
		return self.m_role[0]

	def color_role(self):
		colors = {
			'R':"blue",
			'A':"green",
			'C':"orange",
			'I':"red"
		}
		return colors

	def clean_roles(self):
		tmp = self.m_role.split('|')
		result = list()
		ln = len(self.m_structure.institution.structures_split())

		for t in tmp[:-1]:
			b = self.m_structure.institution.structures_split()[int(t)%ln]
			a = {
				'role':b,
				'letter':b[0],
				'color':self.color_role()[b[0]]
			}
			if a not in result:
				result.append(a)
		return result

	class Meta:
		ordering=('m_structure',)

class Tache(Entity):#PROTECT
	structures = models.ManyToManyField(StructureRole,blank=True)
	structure = models.ForeignKey(Structure,on_delete=models.CASCADE,blank=True,null=True)
	montant = models.FloatField(blank=True,null=True)

	def structures_names(self):
		result = list()
		bool(structs)
		structs = self.structures.filter()
		for r in structs:
			result.append(r.m_structure)
		return result

	def structures_get(self):
		structs = self.structures.filter()
		bool(structs)
		result = list()
		for s in structs:
			result.append(str(s.m_structure.id)+"#"+s.m_structure.nom+"#"+s.m_role)
		result ="§".join(result)
		return result

	def all_structures(self):
		institution = self.structures.first().m_structure.institution
		tmp_structures = institution.structures()
		result = list()
		for s in self.structures.filter():
			if s in tmp_structures:
				result.append(s)
			else:
				result.append("")
		return result

	"""
	def fields(self):
		fields = self.m_fields.split("|")[:-1]
		return fields
	"""

	def type_fields(self):
		fields = self.m_type_fields.split("|")[:-1]
		return fields

	def repartition(self):
		result = None
		reparts = TacheRepartition.objects.filter(m_tache__id=self.id).first()
		if reparts is not None:
			result = reparts.m_roles.filter()
		return result

	def operations(self):
		return Operation.objects.filter(tache__id=self.id).select_related('tache')

	def operations_not_done(self):
		opes = self.operations()
		bool(opes)
		result = list()
		for o in opes:
			if o.rapported() in [None,'0']:
				result.append(o)
		if result == list():
			result = None
		return result

	def operations_done(self):
		opes = self.operations()
		result = list()
		for o in opes:
			tmp = False
			periodes = o.periodes()
			if periodes != None:
				periodes = periodes.desc_split()
				if '2' in periodes:
					tmp = True
					result.append(o)
					continue
				if tmp == False:
					pass
		if result == list():
			result = None
		return result

	def operations_not_done_count(self):
		result = 0
		tmp = self.operations_not_done()
		if tmp == None:
			tmp = list()
		for i in tmp:
			result += 1
		return result

	def operations_done_count(self):
		result = 0
		tmp = self.operations_done()
		if tmp == None:
			tmp = list()
		for i in tmp:
			result += 1
		return result

	def plan_months(self):
		planify = TachePlannify.objects.filter(m_tache__id=self.id).first()
		result = planify
		if result != None:
			result = result.m_planify.split('_')[:-1]
		return result

	def plannification(self):
		result = TachePlannify.objects.filter(m_tache__id=self.id).first()
		return result

	def progression(self,period=None):
		result = 0
		i = 0
		operations = Operation.objects.filter(tache__id=self.id)
		priorites = 0
		bool(operations)
		for o in operations:
			result += (o.progression() )
			"""
			prior_calcul =  o.priority_calcul()
			result *= prior_calcul
			"""
			i += 1

		if i>0:
			result /= i
		return int(result)

	class Meta:
		#ordering=('-date_creation','code',)
		pass

	def evolution_period(self):
		subperiods = self.activite.action.programme.institution.default_subperiod
		result = list()
		for s in range(0,len(subperiods.decoup_desc_slip())):
			tmp=0
			nb_op= 0
			for operation in self.operations():
				"""
				if operation.periodes() != None and operation.periodes().m_chronogramme == subperiods:
					if operation.evolution_period(s) != -1:
						tmp += operation.evolution_period(s)
						nb_op += 1
				"""
				tmp += operation.evolution_period()
				nb_op += 1
			if nb_op != 0:
				tmp /= nb_op
				result.append(tmp)
			else:
				result.append(0)
		return result

	def rapport(self):
		return TacheRapport.objects.filter(m_tache__id = self.id).first()

	def institution(self):
		return self.m_type_entity.get_institution()

	def aggregates2(self):
		tacheAg = TacheAggregate.objects.filter(m_tache__id=self.id).first()
		defaults = self.institution().operations_modules().fill_fields_rapp()
		if tacheAg != None:
			result = list()
			i = 0
			dels = tacheAg.m_values2.split("§")[:-1]

			for d in dels:
				if d in ["#",""," "]:
					result.append(defaults[i]["field"])
				else:
					result.append(d)
				i+=1
		else:
			i = 0
			result = list()
			for d in defaults:
				result.append(defaults[i]["field"])
				i += 1
		return result

class TacheAggregate(models.Model):
	m_tache = models.ForeignKey(Tache,on_delete=models.CASCADE,blank=True,null=True)
	m_values1 = models.TextField() # Champs d'Informations
	m_values2 = models.TextField() # Champs a Rapporter

class Aggregate(models.Model):
	m_institution = models.ForeignKey(Institution,on_delete=models.CASCADE,blank=True,null=True)
	m_nom = models.CharField(max_length=64,blank=True,null=True)
	m_fields = models.TextField(default="",blank=True,null=True)
	m_type_fields = models.TextField(default="",blank=True,null=True)
	# Fields for Rapport
	m_fields_rapported = models.TextField(default="",blank=True,null=True)
	m_type_fields_rapp = models.TextField(default="",blank=True,null=True)
	# Entity for Taches
	m_fields_calculate = models.TextField(default="",blank=True,null=True)
	m_fields_fonction_calculate = models.TextField(default="",blank=True,null=True)
	#fonction 1|nb_fields|function
	m_enum_values = models.TextField(default="",blank=True,null=True)

	def fill_fields(self,rapp=False):
		results = list()
		i = 0
		extras = list()
		if rapp == False:
			a = self.m_type_fields.split("|")
			b = self.m_fields.split("|")
		else:
			a = self.m_type_fields_rapp.split("|")
			b = self.m_fields_rapported.split("|")

		for f in b:
			if a[i] == "choix":
				extras = f.replace("$"," validé")
			else:
				extras = list()
			try:
				results.append({'field':f,'type':a[i],'extras':extras})
				i+=1
			except:
				pass
		return results[:-1]

	def fill_fields_rapp(self):
		return self.fill_fields(True)

	def fields(self):
		fields = self.m_fields.split("|")[:-1]
		return fields

	def fields_rapported(self):
		fields = self.m_fields_rapported.split("|")[:-1]
		return fields

	def type_fields(self):
		fields = self.m_type_fields.split("|")[:-1]
		return fields

	def type_fields_rapported(self):
		fields = self.m_type_fields_rapp.split("|")[:-1]
		return fields
class NatureOperation(models.Model):
    intitule=models.CharField(null=True,blank=True,max_length=255)
    description= models.CharField(null=True,blank=True,max_length=255)
    institution=models.ForeignKey(Institution,null=True,blank=True,on_delete=models.CASCADE)
class CategorieOperation(models.Model):
    intitule=models.CharField(max_length=255,null=True)
    description=models.CharField(null=255,max_length=255)
    institution=models.ForeignKey(Institution,null=True,on_delete=models.CASCADE)
class Operation(models.Model):#PROTECT
	#ano = models.IntegerField(max_length,blank=True,null=True)
	date_debut=models.DateField(null=True)
	code = models.CharField(max_length=255,blank=True,null=True)
	nom = models.TextField(blank=True,null=True)
	m_institution = models.ForeignKey(Institution,on_delete=models.CASCADE,blank=True,null=True)
	periode = models.IntegerField(null=True,blank=True,default=0)
	periode_ok = models.ForeignKey(PeriodeOk,null=True,on_delete=models.CASCADE,blank=True)
	personnel = models.ForeignKey(Personnel,on_delete=models.CASCADE,blank=True,null=True)
	accountable = models.ForeignKey(Personnel,related_name='accountable',on_delete=models.CASCADE,blank=True,null=True)
	consulted =models.ForeignKey(Personnel,related_name='consulted',on_delete=models.CASCADE,blank=True,null=True)
	informed = models.ForeignKey(Personnel,related_name='informed',on_delete=models.CASCADE,blank=True,null=True)
	participant = models.ForeignKey(Personnel,related_name='participant',on_delete=models.CASCADE,blank=True,null=True)


	resultat_attendu = models.TextField(blank=True,null=True)
	etat = models.CharField(max_length=32,default='0')#3 Inactif 4 Mort
	tache = models.ForeignKey(Tache,on_delete=models.CASCADE,blank=True,null=True)
	notification = models.CharField(max_length=128,blank=True,null=True)
	structure = models.ForeignKey(Structure,on_delete=models.CASCADE,null=True,blank=True)
	semaines = models.CharField(max_length=128,blank=True,null=True)
	date_creation = models.DateTimeField(db_index=True,auto_now=True,blank=True,null=True)
	m_tache_plannification = models.CharField(max_length=64,blank=True,null=True)

	statut = models.IntegerField(default=0,null=True)

	montant = models.FloatField(blank=True,null=True,default=0)
	montant2 = models.FloatField(blank=True,null=True,default=0)
	montant3 = models.FloatField(null=True,blank=True,default=0)
	priorite = models.CharField(max_length=64,blank=True,null=True)
	m_value = models.TextField(default="",blank=True,null=True)
	m_value_reported = models.TextField(default="",blank=True,null=True)
	is_RACI = models.IntegerField(blank=True,null=True,default=0)
	dataset=models.ManyToManyField(DataSet)
	m_commentaire = models.TextField(default="",blank=True,null=True)
	nature_operation=models.ForeignKey(NatureOperation,on_delete=models.CASCADE,null=True)
	date_rapported = models.DateTimeField(blank=True,null=True)
	fichier_joint = models.FileField(blank=True,null=True)
	date_echeance = models.DateField(null=True)
	is_deleted = models.BooleanField(null=True,default=False)
	categorie=models.ForeignKey(CategorieOperation,null=True,on_delete=models.CASCADE)
	parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,related_name='children')

	# nature_informed = models.ForeignKey(NatureOperation,on_delete=models.CASCADE,null=True)
	# categorie_informed = models.ForeignKey(CategorieOperation,on_delete=models.CASCADE,null=True)
	

	class Meta:
		db_table= 'ctn_bpf_operation'
	@property
	def delai_restant(self):
		  delai = self.date_echeance - datetime.now().date()
		  total_secondes = int(delai.total_seconds())

		  jours = total_secondes // (24 * 3600)
		  if jours < 0 :
			     resultat = "Le délai est écoulé !"
		  else:

			  	 resultat = f"{jours} jour(s)"
		  return resultat


	def sub_entities(self):
		return list()

	def get_personnel(self):
		result = list()
		if self.is_RACI == 1:
			tmp = OperationRole.objects.filter(m_operation__id=self.id)
			for t in tmp:
				if t.role_racis() in ['R','C']:
					result.append(t.m_personnel)
		else:
			result.append(self.personnel)
		return result0

	def get_doer(self):
		result = list()
		if self.is_RACI == 1:
			tmp = OperationRole.objects.filter(m_operation__id=self.id)
			for t in tmp:
				if t.role_racis() in ['R']:
					result.append(t.m_personnel)
		else:
			result.append(self.personnel)
		return result

	def values_spl1(self):
		values = self.m_value.split("|")[:-1]
		nb_values = len(values)

		fill = self.institution().operations_modules()
		if fill != None:
			fill = fill.fill_fields()
		else:
			fill = list()
		nb_fill = len(fill)
		i = 0
		result = list()
		for f in fill:
			if f['type'] in ['file','image']:
				tmp_file = OperationFile.objects.filter(operation__id=self.id,m_field=f['field']).first()
				if  tmp_file is not None and tmp_file.m_file is not None and tmp_file.m_file.url not in ["",None]:
					if  f['type'] == "image":
						tmp_file = "<a href='"+str(tmp_file.m_file.url)+"'> <img style='width:40px;height:40px;' src='"+str(tmp_file.m_file.url)+"'>' "+str(tmp_file.m_file)+"</a>"
					else:
						tmp_file = "<a href='"+str(tmp_file.m_file.url)+"'> <i class='fas fa-file'></i> &nbsp; "+str(tmp_file.m_file)+" </a>"
				result.append(tmp_file)
			elif f['type'] == 'choix':
				try:
					tmp = values[i].split("\n")
				except:
					tmp = list()
				tmp2 = ""
				for t in tmp:
					tmp2 += "<div class='mb-2'>"+t+"</div>"
				result.append(tmp2)
			else:
				if i < nb_values:
					result.append(values[i])
				else:
					result.append("")
			i+=1
		return result

	def values_spl2(self,decision=False):
		result = list()
		try:
			fill = self.institution().operations_modules().fill_fields(True)
		except:
			fill = list()
		if self.m_value_reported not in [None,""]:
			values = self.m_value_reported.split("|")[:-1]
			i = 0

			for f in fill:
				if f['type'] in ['file','image']:
					tmp_file = OperationFile.objects.filter(operation__id=self.id,m_field=f['field']).first()
					if not decision :
						try:
							if  f['type'] == "image":
								tmp_file = "<a href='"+str(tmp_file.m_file.url)+"'> <img style='width:40px;height:40px;' src='"+str(tmp_file.m_file.url)+"'>' "+str(tmp_file.m_file)+"</a>"
							else:
								tmp_file = "<a href='"+str(tmp_file.m_file.url)+"'> <i class='fas fa-file'></i> &nbsp; "+str(tmp_file.m_file)+" </a>"
						except:
							tmp_file="Aucun Fichier"
					result.append(tmp_file)
				else:
					try:
						result.append(values[i])
					except:
						result.append("")
				i+=1

		else:
			for t in fill:
				result.append(' ')
		return result

	def get_value(self,field):
		fields = self.institution().operations_modules().fill_fields()
		values = self.values_spl1()
		i = 0
		result = -1
		for f in fields:
			if f['field'] == field:
				result = i
				break
			i+=1
		if result != -1:
			if fields[result]["type"] != "choix":
				result = values[result]
			else:
				result =  values[result].split("\r")
		else:
			result = ""
		return result

	def extras(self):
		tmp = self.institution().operations_modules().fill_fields()
		result = list()
		for t in tmp:
			if t['type'] == "choix":
				#ext = ["Lecon 1","Lecon 2","Lecon 3"]
				ext = self.get_value(t['extras']).split("\n")
				result += ext
		return result

	def coef_priority(self):
		coeffs = {"Basse":1,"Normale":2,"Haute":4}

	def agr_fields(self):
		try:
			fields = self.institution().operations_modules().type_fields_rapported()
		except:
			fields = list()
		return fields

	def value_split(self):
		result = list()
		try:
			fields = self.institution().operations_modules().type_fields_rapported()
		except:
			fields = list()
		i=0
		values = self.m_value.split("|")
		for f in fields:
			if f == 'file':
				tmp = OperationFile.objects.filter(operation__id=self.id,m_field=f).first()
				if tmp != None and tmp.m_file != None and tmp.m_file.url != None:
					tmp = tmp.m_file
					result.append("<a href='"+str(tmp.url)+"''> <i class='fas fa-file'> </i> "+str(tmp)+"</a>");
				else:
					result.append(" ")
			else:
				try:
					result.append(values[i])
				except:
					pass

			i+=1
		return result

	def __str__(self):
		return self.nom

	def aggregate_values(self):
		try:
			aggregates = self.institution().operations_modules().fill_fields(True)
		except:
			aggregates = list()
		values = self.values_spl2(True)
		#return values

		i=0
		result = list()
		fieldsa = self.tache.aggregates2()
		for v in aggregates:
			if True:
				result.append({'label':fieldsa[i],'value':values[i]})
				if aggregates[i]['type'] in ['file','image']:
					result[i]['value'] = OperationFile.objects.filter(m_field=aggregates[i]["field"],operation__id=self.id).first()
				elif aggregates[i]['type'] == 'choix':
					reports = values[i].split("-")
					f2 = self.get_value(aggregates[i]['field'])
					result[i]['extras_repported'] = list()
					i2 = 0
					for r in f2:
						result[i]['extras_repported'].append({
							"label":str(r),
							"state":reports[i2]
						})
						i2 += 1
					"""
					result[i]['extras_repported'] = {
						'':,
						'':
					}
					"""
				i+=1
			else:
				pass
		return result

	def evolution_period(self,arg_subperiod="#"):
		actual_subperiod = self.tache.activite.action.programme.institution.default_subperiod
		subperiods = OperationPeriode.objects.filter(m_operation__id=self.id,m_chronogramme=actual_subperiod).first()
		result = -1
		"""
		if subperiods != None and subperiods.desc_split()[arg_subperiod] != '9':# Verifier si tu es different de 9
			tmp = subperiods.desc_split()[int(arg_subperiod)]
			result = self.progression()
		"""
		result = self.progression()
		return round(result,2)

	def progression(self,periode=""):
		result = 0
		institution = self.m_institution
		if institution.repeat_mode == False:
			if self.etat == '2':
				result = 100
		else:
			rapports = self.get_operation_details()
			result = 0
			if rapports.first() != None:
				i = 0
				for r in rapports:
					i+=1
					result += r.progression()
				result /= i
		return round(result,2)

	def priority_calcul(self):
		dicts = {
			"Normale":2,
			"Haute":4,
			"Basse":1,
		}
		if self.priorite != None:
			try:
				result = dicts[self.priorite]
			except:
				result = 2
		else:
			result = 2
		return result

	def have_to_be_rap(self):
		tmp = False
		rapports = self.periodes()
		tmp_rapports = list()
		if rapports != None:
			tmp_rapports = rapports.desc_split()
			tmp_rapports_size = len(tmp_rapports)
			index = 0
		etat = self.etat
		if int(etat) == 0:
			tmp = True
		else:
			tmp = False
		"""
		for i in tmp_rapports:
			if i != '9':
				if i == '0':
					tmp = True
				elif i == '1':
					tmp = False
					break
		"""
		return tmp

	def rap_to_valid(self):
		tmp = False
		rapports = self.periodes()
		tmp_rapports = list()
		if rapports != None:
			tmp_rapports = rapports.desc_split()
			tmp_rapports_size = len(tmp_rapports)
			index = 0
		for i in tmp_rapports:
			if i != '9':
				if i == '1':
					tmp = True
					break
		return tmp

	def periodes(self):
		actual_institution = self.institution()
		if actual_institution != None:
			default_sub = actual_institution.default_subperiod
			result = OperationPeriode.objects.filter(m_operation__id=self.id,m_chronogramme__id=default_sub.id).first()
		else:
			result = OperationPeriode.objects.filter(m_operation__id=self.id).first()
		return result

	def rapported(self):
		result = None
		if self.institution().default_options == True:
			tmp_periods = self.periodes()
			if tmp_periods != None:
				if '0' in tmp_periods.desc_split():
					result = None
				else:
					result = OperationRapport.objects.filter(operation__id=self.id).first()
		else:
			result = self.etat
		return result

	def rapported2(self):
		if '0' in self.periodes().desc_split():
			result = None
		else:
			result = OperationRapport.objects.filter(operation__id=self.id,type_rapport='f').first()
		return result

	def status_op(self):
		result  = ""
		if self.progression() == 100:
			result = "Terminé"
		else:
			if self.rapported() in [None,'0']:
				result = " Non executée "
			else:
				result = "En Attente de Validation"
		return result

	def derniere_modif(self):
		rapport = OperationRapport.objects.filter(operation__id=self.id).first()
		if rapport == None:
			result = self.date_creation
		else:
			result = rapport.date_creation
		return result

	def tech_rapports(self):
		return OperationRapport.objects.filter(operation__id=self.id,type_rapport='c')

	def finan_rapports(self):
		return OperationRapport.objects.filter(operation__id=self.id,type_rapport='f')

	def institution2(self):
		if self.tache != None:
			entity_type = InsitutionEntities.objects.filter(m_entity_type=self.tache.m_type_entity).first()
		else:
			entity_type = None
		result = None
		if entity_type != None:
			result = entity_type.m_institution
		return result

	def institution(self):
		return self.m_institution

	class Meta:
		ordering=('nom','date_creation',)

	def raci_roles(self):
		return OperationRole.objects.filter(m_operation__id=self.id)

	def raci_history(self):
		pass

	def get_operation_details(self):
		return OperationDetails.objects.filter(m_operation__id = self.id)

	def get_operation_details_invalid(self):
		return OperationDetails.objects.filter(m_operation__id = self.id,etat="1")

	def get_operation_details_valid(self):
		return OperationDetails.objects.filter(m_operation__id = self.id,etat="2")


class HistoricRACI(models.Model):
	m_operation= models.ForeignKey(Operation,on_delete=models.CASCADE,blank=True,null=True)
	m_role = models.CharField(max_length=255,blank=True,null=True)
	m_commentaire=models.TextField(blank=True,null=True)
	m_date_realisation = models.DateTimeField(auto_now_add=True)
	file=models.FileField(blank=True,null=True)
	mail=models.CharField(null=True,max_length=255,blank=True)

class OperationDetails(models.Model):
	m_operation = models.ForeignKey(Operation,on_delete=models.CASCADE,blank=True,null=True)
	m_value_reported = models.TextField(blank=True,null=True)
	m_date_realisation = models.DateTimeField(blank=True,null=True)
	date_created = models.DateTimeField(auto_now=True)
	m_commentaire =  models.TextField(blank=True,null=True)
	# RACI Fields Organisation
	personnel = models.ForeignKey(Personnel,on_delete=models.SET_NULL,blank=True,null=True)
	accountable = models.ForeignKey(Personnel,related_name='accountable_2',on_delete=models.SET_NULL,blank=True,null=True)
	consulted =models.ForeignKey(Personnel,related_name='consulted_2',on_delete=models.SET_NULL,blank=True,null=True)
	informed = models.ForeignKey(Personnel,related_name='informed_2',on_delete=models.SET_NULL,blank=True,null=True)
	m_institution_id=models.ForeignKey(Institution,on_delete=models.SET_NULL,null=True)
	is_deleted = models.BooleanField(null=True,default=False)
	# Etat Visualisation
	etat = models.CharField(max_length=32,default='0')#3 Inactif 4 Mort

	def progression(self):
		result = 0
		if self.etat == "2":
			result = 100
		return result

	def __str__(self):
		return "Rapport du : "+str(self.date_created.date())

	def institution(self):
		return self.m_operation.institution()

	def values_spl2(self,decision=False):
		result = list()
		if True:
			fill = self.m_operation.institution().operations_modules().fill_fields(True)
		else:
			fill = list()
		if self.m_value_reported not in [None,""]:
			values = self.m_value_reported.split("|")[:-1]
			i = 0

			for f in fill:
				if f['type'] in ['file','image']:
					tmp_file = OperationDetailsFile.objects.filter(operation__id=self.id,m_field=f['field']).first()
					if not decision :
						try:
							if  f['type'] == "image":
								tmp_file = "<a href='"+str(tmp_file.m_file.url)+"'> <img style='width:40px;height:40px;' src='"+str(tmp_file.m_file.url)+"'>' "+str(tmp_file.m_file)+"</a>"
							else:
								tmp_file = "<a href='"+str(tmp_file.m_file.url)+"'> <i class='fas fa-file'></i> &nbsp; "+str(tmp_file.m_file)+" </a>"
						except:
							tmp_file="Aucun Fichier"
					result.append(tmp_file)
				else:
					try:
						result.append(values[i])
					except:
						result.append("")
				i+=1

		else:
			for t in fill:
				result.append(' ')
		return result


	def aggregate_values(self):
		try:
			aggregates = self.institution().operations_modules().fill_fields(True)
		except:
			aggregates = list()
		values = self.values_spl2(True)
		fieldsa = self.m_operation.tache.aggregates2()
		#return values

		i=0
		result = list()
		for v in aggregates:
			try:
				result.append({'label':fieldsa[i],'type':aggregates[i]["type"],'value':values[i]})
				if aggregates[i]['type'] in ['file','image']:
					result[i]['value'] = OperationDetailsFile.objects.filter(m_field=aggregates[i]["field"],operation__id=self.id).first()
				elif aggregates[i]['type'] == 'choix':
					reports = values[i].split("-")
					f2 = self.get_value(aggregates[i]['field'])
					result[i]['extras_repported'] = list()
					i2 = 0
					for r in f2:
						result[i]['extras_repported'].append({
							"label":str(r),
							"state":reports[i2]
						})
						i2 += 1
				i+=1
			except:
				pass
		return result

class OperationDetailsFile(models.Model):
	m_field = models.CharField(max_length=32,blank=True,null=True)
	m_file = models.FileField(blank=True,null=True)
	operation = models.ForeignKey(OperationDetails,on_delete=models.CASCADE,blank=True,null=True)

class OperationConsulted(models.Model):
	m_operation = models.ForeignKey(Operation,on_delete=models.CASCADE,blank=True,null=True)

	m_observations = models.TextField(blank=True,null=True)
	email1 = models.CharField(null=True,max_length=58)
	email2 = models.CharField(null=True,max_length=58)
	email3 = models.CharField(null=True,max_length=50)
	email4 = models.CharField(null=True,max_length=59)

	file = models.FileField(null=True)



class OperationFile(models.Model):
	m_field = models.CharField(max_length=32,blank=True,null=True)
	m_file = models.FileField(blank=True,null=True)
	operation = models.ForeignKey(Operation,on_delete=models.CASCADE,blank=True,null=True)

class OperationEval(models.Model):
	operation_rapport = models.ForeignKey(Operation,on_delete=models.CASCADE,blank=True,null=True)
	date_creation = models.DateTimeField(db_index=True,auto_now_add=True)
	commentaire = models.TextField(blank=True,null=True)
	m_status = models.IntegerField(default=0,blank=True,null=True)
	m_values = models.TextField(blank=True,null=True)

class OperationRapport(models.Model):
	operation = models.ForeignKey(Operation,on_delete=models.CASCADE,blank=True,null=True)
	piece_jointe = models.FileField(blank=True,null=True)
	nom_piece_jointe = models.CharField(max_length=128,blank=True,null=True)
	date_creation = models.DateTimeField(db_index=True,auto_now_add=True)
	commentaire = models.TextField(blank=True,null=True)
	type_rapport = models.CharField(default="c",max_length=2,blank=True,null=True)#c technique, f financier
	period = models.IntegerField(blank=True,null=True),
	etat = models.IntegerField(null=True,blank=True,default=0)
	def __str__(self):
		if self.piece_jointe != None:
			result = self.piece_jointe.name
		else:
			result = self.nom_piece_jointem
		return str(result)

class OperationRapport_Eval(models.Model):
	operation_rapport = models.ForeignKey(OperationRapport,on_delete=models.CASCADE,blank=True,null=True)
	date_creation = models.DateTimeField(db_index=True,auto_now_add=True)
	commentaire = models.TextField(blank=True,null=True)
	m_status = models.IntegerField(default=0,blank=True,null=True)

class TacheRepartition(models.Model):
	m_tache = models.ForeignKey(Tache,on_delete=models.CASCADE,blank=True,null=True)
	m_personnels = models.ManyToManyField(Personnel,blank=True)
	m_roles = models.ManyToManyField(Role,blank=True)

class TachePlannify(models.Model):
	m_tache = models.ForeignKey(Tache,on_delete=models.CASCADE,blank=True,null=True)
	m_planify = models.TextField(blank=True,null=True)
	m_periode = models.ForeignKey(Periode,on_delete=models.SET_NULL,blank=True,null=True)
	m_value = models.CharField(blank=True,null=True,max_length=256)
	def __str__(self):
		return str(self.m_periode) + " : "+str(self.m_planify)
	def table(self):
		result = self.m_planify.split("_")
		if result != []:
			result = result[:-1]
		return result
	def index(self):
		result = list()
		tmp = self.m_periode.decoup_slip()
		for t in self.table():
			i = 0
			for s in tmp:
				if s == t:
					result.append((i+1))
					break
				i+=1
		return result

class TachePeriode(models.Model):
	m_tache = models.ForeignKey(Tache,on_delete=models.CASCADE,blank=True,null=True)
	m_chronogramme = models.ForeignKey(Periode,on_delete=models.SET_NULL,blank=True,null=True)

class OperationPeriode(models.Model):
	m_operation= models.ForeignKey(Operation,on_delete=models.CASCADE,blank=True,null=True)
	m_chronogramme = models.ForeignKey(SubPeriode,on_delete=models.SET_NULL,blank=True,null=True)
	m_desc_realisation = models.TextField(blank=True,null=True)

	def details_periode(self):
		periode_tache = self.m_operation.m_tache_plannification
		actual = self.chrono_split()
		decoup = self.desc_split()
		i = -1
		for d in decoup:
			i+=1
			if int(d) != 9:
				break
		if i != -1:
			tmp = periode_tache + " - "+ actual[i]
		else:
			tmp = None
		return tmp

	def actu_value(self):
		plannify = self.m_operation.m_tache_plannification
		periode = self.m_operation.institution().default_period

		tmp_val = get_period_values(periode,plannify+"_")[0]

		ta1 = datetime.date(int(tmp_val[:4]),int(tmp_val[4:6]),int(tmp_val[6:8]))
		ta2 = datetime.date(int(tmp_val[8:12]),int(tmp_val[12:14]),int(tmp_val[14:16]))
		ta3 = ta2
		test = ta2.isoweekday()
		if test > 1 :
			ta2 -= datetime.timedelta(test-1)
			ta3 += datetime.timedelta(7-test)
		test_dates =list()
		for i in range(5):
			test_dates.append("Du "+str(ta2)+" Au "+str(ta3))
			ta2 += datetime.timedelta(7)
			ta3 += datetime.timedelta(7)
		bumps1 = [int(tmp_val[:4]),int(tmp_val[4:6])-1,int(tmp_val[6:8])]
		bumps2 = [int(tmp_val[8:12]),int(tmp_val[12:14])-1,int(tmp_val[14:16])]

		descREAL = self.m_desc_realisation.split("_")
		for i in range(5):
			if descREAL[i] == "0":
				test_dates=test_dates[i]
				break
		return test_dates

	def chrono_split(self):
		return self.m_chronogramme.m_decoupage.split("|")
	def desc_split(self):
		result = None
		if self.m_desc_realisation != None:
			result = self.m_desc_realisation.split("_")[:-1]
		return result
	def __str__(self):
		return str(self.m_desc_realisation)

#Hierachie Rapports
"""
class TacheRapport(models.Model):
	m_activite = models.ForeignKey(Activite,on_delete=models.CASCADE,blank=True,null=True)
	m_date_rapport = models.DateTimeField(db_index=True,auto_now_add=True)
	m_resultat_realise = models.TextField(blank=True,null=True)
"""
class OperationRole(models.Model):
	m_name = models.CharField(max_length=128,blank=True,null=True)
	m_operation = models.ForeignKey(Operation,on_delete=models.CASCADE,blank=True,null=True)
	m_personnel = models.ForeignKey(Personnel,on_delete=models.CASCADE,blank=True,null=True)
	def __str__(self):
		return "RACI" + " " + str(self.m_operation) + " " + str(self.m_personnel)

	def sub_entities(self):
		return list()

	def role_racis(self):
		roles = ['R','A','C','I']
		i = 0
		result = list()
		try:
			for r in self.m_name.split("|"):
				if r == '1':
					result.append(roles[i])
				i+=1
		except:
			pass
		if result != list():
			result = result[0]
		return result

	def details_role(self):
		rl = self.role_racis()
		if rl == list():
			rl = "#"
		results = {
			'#':" ",
			'R':"Responsable de l'Execution",
			'A':"Chargé de la Validation",
			'C':"Aide à la Réalisation et à la Vérification",
			'I':" Rapporteur et Point Focal des Informations"
		}
		return results[rl]

class EntityRapport(models.Model):
	m_entity = models.ForeignKey(Entity,on_delete=models.CASCADE,blank=True,null=True)
	m_date_rapport = models.DateTimeField(db_index=True,auto_now_add=True)
	m_resultat_realise = models.TextField(blank=True,null=True)

class InsitutionEntities(models.Model):#PROTECT
	m_institution = models.ForeignKey(Institution,on_delete=models.CASCADE,blank=True,null=True)
	m_entity_type = models.ForeignKey(EntityType,on_delete=models.CASCADE,blank=True,null=True)
	#OneToOneField
	m_hierachie = models.IntegerField(blank=True,null=True)
	dataset = models.ManyToManyField(DataSet)
	class Meta:
		ordering=('m_institution','m_hierachie',)
	def __str__(self):
		#str(self.m_institution) + " : "+str(self.m_entity_type) + " - " + str(self.m_hierachie)
		return str(self.m_entity_type)

	def hierachie_lvl(self):
		hierachies = InsitutionEntities.objects.filter(m_institution=self.m_institution).select_related('m_institution').last().m_hierachie
		lvl = hierachies - self.m_hierachie
		return lvl

#External Models for Opera
class OperaFile(models.Model):
	m_name = models.CharField(max_length=128,blank=True,null=True)
	m_file = models.FileField(blank=True,null=True)
	m_category = models.CharField(max_length=128,blank=True,null=True)

	m_date_creation = models.DateTimeField(db_index=True,auto_now_add=True)
	m_description = models.TextField(blank=True,null=True)
	m_institution = models.ForeignKey(Institution,on_delete=models.CASCADE,blank=True,null=True)

	is_public = models.IntegerField(blank=True,null=True)
	class Meta:
		ordering=('-m_date_creation',)
	def __str__(self):
		return str(self.m_name)
	def extension(self):
		return self.m_file.name[-3:]

class Temoignage(models.Model):
	"""docstring for Temoignage"""
	m_picture = models.FileField(blank=True,null=True)
	m_name = models.CharField(max_length=64,blank=True,null=True)
	m_poste = models.CharField(max_length=64,blank=True,null=True)
	m_description = models.TextField(blank=True,null=True)

class Assistance(models.Model):
	m_user = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
	m_date_creation = models.DateTimeField(db_index=True,auto_now_add=True)
	m_message = models.TextField(blank=True,null=True)

class OperaApp(models.Model):
	"""docstring for Temoignage"""
	m_picture = models.FileField(blank=True,null=True)
	m_name = models.CharField(max_length=64,blank=True,null=True)
	m_description = models.TextField(blank=True,null=True)
	is_online = models.BooleanField(default=False, blank=True,null=True)
	m_website = models.CharField(max_length=64,blank=True,null=True)

#External Models for Opera

class InstitutionDecoupage(models.Model):
	m_institution = models.ForeignKey(Institution,on_delete=models.CASCADE,blank=True,null=True)
	m_periode = models.ForeignKey(Periode,on_delete=models.SET_NULL,blank=True,null=True)
	m_decoupage = models.TextField(blank=True,null=True)
	all_selected = models.BooleanField(blank=True,null=True,default=True)

class IndicateurVal(models.Model):
	m_indicateur = models.ForeignKey(Indicateur,on_delete=models.SET_NULL,blank=True,null=True)
	m_periode  = models.CharField(max_length=128,blank=True,null=True)
	m_date_created = models.DateTimeField(auto_now=True,blank=True,null=True)
	m_personnel = models.ForeignKey(Personnel,on_delete=models.CASCADE,blank=True,null=True)
	def value_calcul(self):
		ind = self.m_indicateur.m_datalets_calcul
		a = ""
		if ind != None:
			ind = ind.replace("$"+str(self.m_numerateur.id)+"$",str(self.m_valeur))
			#ind = ind.replace("$"+str(self.m_indicateur.indi_denum().id)+"$",str(self.m_indicateur.indi_denum().m_default_value) )
			#a = eval(ind)
		return a

	def elements(self):
		return IndicateurValElements.objects.filter(m_indicateurval__id=self.id)

	def __str__(self):
		return str(self.m_indicateur)

# Messages Section ====================================================================================
class Message(models.Model):
	m_sender = models.ForeignKey(Personnel,on_delete=models.SET_NULL,blank=True,null=True)
	m_content = models.TextField(blank=True,null=True)
	m_date_send= models.DateTimeField(auto_now=True,blank=True,null=True)

class MessageDestinators(models.Model):
	m_message = models.ForeignKey(Message,on_delete=models.SET_NULL,blank=True,null=True)
	m_destinators = models.ForeignKey(Personnel,on_delete=models.SET_NULL,blank=True,null=True)
# Messages Section ====================================================================================


class IndicateurValElements(models.Model):
	m_indicateurval = models.ForeignKey(IndicateurVal,on_delete=models.SET_NULL,blank=True,null=True)
	m_data_element = models.ForeignKey(DataElement,on_delete=models.SET_NULL,blank=True,null=True)
	m_valeur = models.CharField(max_length=128,blank=True,null=True)
	# history = AuditlogHistoryField()
	def __str__(self):
		return str(self.m_indicateurval) + self.m_valeur

class PersonnelRACI(models.Model):
	m_personnel = models.ForeignKey(Personnel,blank=True,null=True,on_delete=models.CASCADE)
	m_entity = models.ForeignKey(Entity,blank=True,null=True,on_delete=models.CASCADE)
	m_roles = models.TextField(blank=True,null=True)
	# history = AuditlogHistoryField()
	def __str__(self):
		return str(self.m_personnel) +" - "+str(self.m_entity)

	def RACI_detail(self):
		dts = self.m_roles.split("|")
		class RACIELT:
			def __init__(self,role,color="secondary"):
				self.m_role = role
				self.m_color=color
			self.m_status = 0

			def __str__(self):
				return self.m_role

		result = [RACIELT("R","success"),RACIELT("A","danger"),RACIELT("C","primary"),RACIELT("I","warning")]
		for i in range(4):
			if dts[i] == "1":
				result[i].m_status = 1
		return result
class Categorie(models.Model):
	nom=models.CharField(max_length=255,null=True,blank=True)
	institution=models.ForeignKey(Institution,null=True,on_delete=models.CASCADE)
	# history = AuditlogHistoryField()

class Sous_categorie(models.Model):
	categorie=models.ForeignKey(Categorie,on_delete=models.CASCADE, null=True,blank=True)
	nom=models.CharField(max_length=255, null=True,blank=True)
	institution = models.ForeignKey(Institution,on_delete=models.CASCADE,null=True, blank=True)
	# history = AuditlogHistoryField()
class Archive(models.Model):
	titre=models.CharField(max_length=255,null=True)
	format_fichier=models.CharField(max_length=255,null=True)
	auteur = models.CharField(max_length=255,null=True)
	date_enregistrement = models.DateTimeField(null=True,blank=True)
	description = models.CharField(null=True,blank=True,max_length=255)
	file = models.FileField(null=True,blank=True)
	categorie=models.ForeignKey(Categorie,null=True,blank=True,on_delete=models.CASCADE)
	institution=models.ForeignKey(Institution,null=True,on_delete=models.CASCADE)

	taille = models.IntegerField(null=True, blank=True)

	unite  = models.CharField(null=True, blank=True, max_length=255)

	sous_categorie=models.ForeignKey(Sous_categorie,on_delete=models.CASCADE, null=True, blank=True)

	source_financement = models.CharField(max_length=255,null=True, blank=True)

	provenance = models.TextField(null=True,blank=True)
	# history = AuditlogHistoryField()
	index = models.TextField(blank=True,null=True)

	is_public = models.BooleanField(null=True,blank=True)

	# is_public = models.BooleanField()


class IndicateurValeur(models.Model):
	periode_ok = models.ForeignKey(PeriodeOk,null=True,blank=True,on_delete=models.CASCADE)
	indicateur = models.ForeignKey(Indicateur,null=True,blank=True,on_delete=models.CASCADE)
	valeur = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	type_donnee = models.CharField(null=True,blank=True, max_length=255)
	institution = models.ForeignKey(Institution,on_delete=models.CASCADE,null=True,blank=True)

	date_enregistrement = models.DateField(null=True,blank=True)

	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
	# history = AuditlogHistoryField()
	structure = models.ForeignKey(Structure,on_delete=models.CASCADE, null=True,blank=True)
	date_saisie = models.DateField(null=True)
	valeur_cumulee = models.IntegerField(null=True)
	valeur_moyenne = models.IntegerField(null=True)

	# auditlog.register(Categorie)
	# auditlog.register(Sous_categorie)


class ConsultationLog(models.Model):
	document_id = models.IntegerField()
	user_ip = models.CharField(max_length=45)
	consultation_datetime = models.DateTimeField()
	user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
class Rubrique(models.Model):
	nom = models.CharField(max_length=255,null=True,blank=True)

class Sous_Rubrique(models.Model):
	nom = models.CharField(max_length=255,null=True,blank=True)
	rubrique = models.ForeignKey(Rubrique,on_delete=models.CASCADE,null=True,blank=True)



class Actualite(models.Model):
	intitule = models.CharField(null=True,blank=True,max_length=255)
	description = models.TextField(null=True,blank=True)
	photos = models.FileField(null=True,blank=True)
	documents = models.FileField(null=True,blank=True)
	rubrique = models.ForeignKey(Rubrique,on_delete=models.CASCADE,null=True,blank=True)
	sous_rubrique = models.ForeignKey(Sous_Rubrique,on_delete=models.CASCADE,null=True,blank=True,related_name='actualites')
	date = models.DateField(null=True,blank=True)
	is_public = models.BooleanField(null=True)
	hash_code = models.CharField(max_length=255,null=True)
	
	institution= models.ForeignKey(Institution,on_delete=models.CASCADE,null=True,related_name='actualites')
	#id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	prix = models.IntegerField(null=True)

	class Meta:
		indexes = [
			models.Index(fields=['institution','intitule','prix'],name='institutions_index')
		]

# class Sous_Actualite(models.Model):
# 	actualite = models.ForeignKey(Actualite,on_delete=models.CASCADE,null=True,blank=True)
# 	nom = models.CharField(null=True,blank=True,max_length=255)
class SousActualite(models.Model):
    intitule = models.CharField(null=True, max_length=255)
    description = models.TextField(null=True)
    photos = models.ImageField(upload_to="generate_filename", blank=True, null=True)
    documents = models.FileField(upload_to="generate_filename", blank=True, null=True)
    actualite = models.ForeignKey(Actualite, null=True, on_delete=models.CASCADE)
    baniere = models.ForeignKey(Baniere, on_delete=models.CASCADE, null=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True, blank=True)
    sexe = models.CharField(max_length=255, null=True)
    prix = models.IntegerField(null=True)
    tranche = models.CharField(max_length=255, null=True)
    colors = models.CharField(null=True, max_length=255)

    class Meta:
        indexes = [
            models.Index(
                fields=['intitule', 'actualite', 'institution', 'prix'],
                name='index_sous_actualite'
            )
        ]



# class GroupeElement(models.Model):
#     dataelement = models.ForeignKey(DataElement,on_delete=models.CASCADE,null=True)
#     qte_declare = models.IntegerField(null=True)
#     qte_valide = models.IntegerField(null=True)
#     cout_unitaire = models.IntegerField(null=True)
#     montant=models.IntegerField(null=True)
    
    
    # class Meta:
    #     unique_together = (('dataelement'),)
        

class MasterGroupe(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255,null=True,blank=True)
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE,null=True,blank=True)

class Master(models.Model):
    nom = models.CharField(max_length=255,null=True,blank=True)
    institution = models.ForeignKey(Institution,null=True,blank=True,on_delete=models.CASCADE)
    master_groupe = models.ForeignKey(MasterGroupe,on_delete=models.CASCADE,null=True,blank=True)

class MasterElement(models.Model):
    master = models.ManyToManyField(Master)
    type = models.CharField(null=True,blank=True,max_length=255)
    element = models.ManyToManyField(DataElement)
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE,null=True,blank=True)


class DataAccreditation(models.Model):
    institution=models.ForeignKey(Institution,null=True,on_delete=models.CASCADE)
    region= models.TextField(null=True,blank=True)
    district=models.TextField(null=True,blank=True)
    aire=models.TextField(null=True,blank=True)
    fosa = models.TextField(null=True,blank=True)
    status_fosa=models.TextField(max_length=255,null=True)
    fonction= models.TextField(null=True,blank=True)
    thematique=models.TextField(null=True,blank=True)
    critere=models.TextField(null=True,blank=True)
    numero=models.IntegerField(null=True,blank=True)
    critere_consensus=models.TextField(null=True,blank=True)
    poids=models.IntegerField(null=True,blank=True)   
    pas_du_tout_noter_0=models.IntegerField(null=True,blank=True)
    partiel_noter_1=models.IntegerField(null=True,blank=True)
    entierement_noter_2=models.IntegerField(null=True,blank=True)
    total_points=models.IntegerField(null=True,blank=True)
    total_max=models.IntegerField(null=True,blank=True) 
    score=models.IntegerField(null=True,blank=True)
    type=models.TextField(null=True,blank=True)
  
# class BaniereActualite(models.Model):
#     actualite = models.ForeignKey(Actualite,null=True,on_delete=models.CASCADE)
#     baniere = models.ForeignKey(Baniere,null=True,on_delete=models.CASCADE)
# class Meta:
#         unique_together = ('baniere', 'actualite')

class Faq(models.Model):
	intitule = models.CharField(null= True,max_length=255,blank=True)
	description = models.TextField(null=True,blank=True)
	logo = models.FileField(null=True,blank=True)
	