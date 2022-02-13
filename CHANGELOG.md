# Changelog

## v2.1.2

- minor changes and support for latest python versions
- now "created" and "updated" fields will be included in generated models
- minor bug fixes

## v2.1.0

With v2.1.0 you get:

- we generate **factories** for your models based on factory_boy 🤖
- we generate **tests** for your factories based on Pytest ✨
- we put your core tests under **tests/core/$app_name** and your api tests under **tests/apis/$app_name** 💅

> next version will include API endpoints tests

## v2.0.2

With v2.0.2 you get:

- sorted & elegant imports in your generated files 🤖
- better line breaks and code formatting ✨
- nice colored outputs 💅

## v2.0.1

With v2.0.1 you get sorted elegant imports in your generated files out of the box, using the power of `isort` 🤖

## v2.0.0

With this version, we added support for **ViewSets** using **Mixins** 🥳 🎉

- Customize your ViewSets on the fly with `--mixins CRUD` ⚡ .
- Wanna only support Create, Read and Update ? pass `--mixins CRU`, customize your view in any way you like.
- **C** is for `create` **R** is for `list` and retrieve **U** is `update` and **D** is `destroy` as you might guess.
- One more thing ... we generate your actions along with everything you'd need inside and your get_queryset(), get_object() and more 🚀 🤖 .
- We still **support** ModelViewSets as well, if you want them just drop the `--mixins` option.

here is a ViewSet example generated with the help of `--mixins CR`:

```python
class AuthorViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    #permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        #user = self.request.user
        queryset = Author.objects.all()
        #insert specific queryset logic here
        return queryset

    def get_object(self):
        #insert specific get_object logic here
        return super().get_object()

    def create(self, request, *args, **kwargs):
        serializer = AuthorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = AuthorSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AuthorSerializer(instance=instance)
        return Response(serializer.data)
```

## v1.4.2

- Tested for different API structures 🏗️
- Code coverage at 100% again 👀
- Improvements by contributors 👍🏻

## V1.3.0

- Added `CORE_FOLDER` and `API_FOLDER` settings in order to organize code and separate concerns in our APIs:

```py
CORE_FOLDER = "my_core_folder_path/" # you can leave them empty
API_FOLDER = "my_api_folder_path/"   # or set them to be the same
```

- Core folder is for `models.py` `admin.py` and `migrations`
- API folder will contain `views.py` `serializers.py` and `urls.py`

## v1.0.1

- minor typo fix with URLs

## v1.0.0

- 100 % full test coverage 🚀
- Major changes and improvements 👍🏻
- Code quality and linting with pylint ✅
- CI/CD with travisCI 🏆

## v1.0-beta.1

- changes (Pre-release)

## v0.6-alpha

- few improvments
