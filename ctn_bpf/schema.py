import graphene  
from ctn_bpf.models import Operation  
from ctn_bpf.models import DataSet
from graphene_django import DjangoObjectType
from ctn_bpf.models import Personnel
from ctn_bpf.models import Structure
from ctn_bpf.models import PeriodeOk
from ctn_bpf.models import Institution
from ctn_bpf.models import Archive
from ctn_bpf.models import Entity
from ctn_bpf.models import InsitutionEntities
from ctn_bpf.models import Indicateur
from ctn_bpf.models import DataSet
import django_filters
import graphene
from graphene import relay
class IndicateurType(DjangoObjectType):
    class Meta:
        model = Indicateur
        fields = '__all__'  # Vous pouvez spécifier les champs comme ('id', 'name') pour plus de clarté


class DataSetType(DjangoObjectType):
    class Meta:
        model = DataSet
        fields = "__all__"

    

class PersonnelType(DjangoObjectType):
    class Meta:
        model = Personnel
        fields = '__all__'

    
    
  
class StructureType(DjangoObjectType):
    class Meta:
        model = Structure
        fields = '__all__'  # Vous pouvez spécifier les champs comme ('id', 'name') pour plus de clarté



    
class PeriodeOkType(DjangoObjectType):
    class Meta:
        model = PeriodeOk
        interfaces = (relay.Node,)
        fields = ('id', 'nom')  # Assurez-vous que ces champs sont inclus

   

class OperationType(DjangoObjectType):  
    class Meta:  
        model = Operation  
        fields = "__all__"  


class InsitutionEntitiesType(DjangoObjectType):
    class Meta:

        model = InsitutionEntities
        fields = '__all__'
class InstitutionType(DjangoObjectType):
    class Meta:
        model = Institution
        fields = '__all__'
class ArchiveType(DjangoObjectType):
    class Meta:
        model = Archive
        fields = '__all__'
class Query(graphene.ObjectType):  
    operations = graphene.List(OperationType, id=graphene.Int(), name=graphene.String())  # Add parameters as needed  
    structures = graphene.List(StructureType, id=graphene.Int(), name=graphene.String())
    insitutionentity = graphene.List(InsitutionEntitiesType)

    indicateur = graphene.List(IndicateurType)

    institution = graphene.List(InstitutionType)

    annee = graphene.List(PeriodeOkType)
    dataset = graphene.List(DataSetType)
    personnel = graphene.List(PersonnelType)
    archives = graphene.List(ArchiveType)



   
    def resolve_indicateur(self,info):
        return Indicateur.objects.all()

    def resolve_archives(self,info):
        return Archive.objects.all()
    def resolve_institution(self,info):
        return Institution.objects.all()
    def resolve_insitutionentity(self,info):
        return InsitutionEntities.objects.all()
    def resolve_operations(self, info, id=None, name=None):  
        queryset = Operation.objects.all()  
        if id:  
            queryset = queryset.filter(id=id)  
        if name:  
            queryset = queryset.filter(name__icontains=name)  

        return queryset  
    def resolve_structures(self, info, id=None, name=None):
        queryset = Structure.objects.all()

        if id is not None:  # Vérification explicite pour None
            queryset = queryset.filter(id=id)

        if name:  # Cela vérifie à la fois None et les chaînes vides
            queryset = queryset.filter(name__icontains=name)

        return queryset
    def resolve_annee(self,info):
        return PeriodeOk.objects.all()
        
    

    def resolve_dataset(self,info):
        return DataSet.objects.all()
    

    def resolve_personnel(sel,info):
        return Personnel.objects.all()



class create_operation(graphene.Mutation):
    class Arguments:
    
        nom=graphene.String(required=True)

    operation = graphene.Field(OperationType)
    
    def mutate(self,info,nom):
        operation = Operation(nom=nom)
        operation.save()
        return create_operation(operation=operation)

class create_annee(graphene.Mutation):
    class Arguments:
        nom = graphene.String(required=True)

    # Définissez le type de retour de la mutation
    annee = graphene.Field(PeriodeOkType)

    def mutate(self, info, nom):
        # Créez une nouvelle instance de PeriodeOk
        annee = PeriodeOk(nom=nom)
        annee.save()

        # Retournez l'objet annee de type PeriodeOkType
        return create_annee(annee=annee)

class delete_operation(graphene.Mutation):

    class Arguments:
        id = graphene.ID(required=True)
    id = graphene.Int()
    def mutate(self, info, id):
        operation = Operation.objects.get(pk=id)
        operation.delete()
        return delete_operation(id=id)

class delete_annee(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    id = graphene.Int()

    def mutate(self,info,id):
        annee = PeriodeOk.objects.get(id=id)
        annee.delete()
        return delete_annee(id=id)

class delete_indicateur(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    id=graphene.Int()
    def mutate(self, info, id):
        indicateur = Indicateur.objects.get(id=id)
        indicateur.delete()
        return delete_indicateur(id=id)

# class update_operation(graphene.Mutation):
#     graphene.Field(OperationType, id=graphene.ID(required=True), nom=graphene.String())
# class delete_operation(graphene.Mutation):

#     graphene.Field(OperationType, id=graphene.ID(required=True))


    


  
class Mutation(graphene.ObjectType):
    create_operation = create_operation.Field()
    create_annee = create_annee.Field()
    delete_operation = delete_operation.Field()
    delete_annee = delete_annee.Field()
    delete_indicateur = delete_indicateur.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)
