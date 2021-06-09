# from tijdschrijven.models import Project
# from django_cte import CTEManager, With

# from django.db.models import F, Value, TextField, IntegerField
# from django.db.models.functions import Concat


# def geefProjectChildren(ProjectID):

#     def geef_project_children(childs):

#         return Project.objects.filter(
#             # start with root nodes
#             id=ProjectID

#         ).values(
#             "id",
#             "ParentID",
#             path=F("id"),
#             depth=Value(0, output_field=IntegerField()),
#         ).union(
#             # recursive union: get descendants
#             childs.join(Project, ParentID=childs.col.id).values(
#                 "id",
#                 "ParentID",
#                 path=Concat(
#                     childs.col.path, Value(";",output_field=TextField()) ,Value("\x01"), F("id"),
#                     output_field=TextField(),
#                 ),
#                 depth=childs.col.depth - Value(1, output_field=IntegerField()),
#             ),
#             all=True,
#         )
#     childs = With.recursive(geef_project_children)

#     return (childs.join(Project, id=childs.col.id)
#                     .with_cte(childs)
#                     .annotate(
#                         path=childs.col.path,
#                         depth=childs.col.depth,
#                     )
#                     .order_by("-depth")
#                 )

# def geefProjectParents(ProjectID):

#     # hoe gaan we om met null   
 
#     def geef_project_parents(parents):
#         return Project.objects.filter(
#             # start with root nodes
#             id = ProjectID
#         ).values(
#             "id",
#             "ParentID",
#             path=F("id"),
#             depth=Value(0, output_field=IntegerField()),
#         ).union(
#             # recursive union: get ancestors
#             parents.join(Project, id=parents.col.ParentID_id).values(
#                 "id",
#                 "ParentID",
#                 path=Concat(
#                     parents.col.path, Value(";",output_field=TextField()) ,Value("\x01"), F("id"),
#                     output_field=TextField(),
#                 ),
#                 depth=parents.col.depth + Value(1, output_field=IntegerField()),
#             ),
#             all=True,
#         )   

#     parents = With.recursive(geef_project_parents)

#     return (parents.join(Project, id=parents.col.id)
#                     .with_cte(parents)
#                     .annotate(
#                         path=parents.col.path,
#                         depth=parents.col.depth,
#                     )
#                     .order_by("-depth")
#                 )