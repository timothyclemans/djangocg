from __future__ import absolute_import

from operator import attrgetter

from djangocg.contrib.contenttypes.models import ContentType
from djangocg.contrib.sessions.backends.db import SessionStore
from djangocg.db.models import Count
from djangocg.db.models.loading import cache
from djangocg.test import TestCase

from .models import (ResolveThis, Item, RelatedItem, Child, Leaf, Proxy,
    SimpleItem, Feature, ItemAndSimpleItem)


class DeferRegressionTest(TestCase):
    def test_basic(self):
        # Deferred fields should really be deferred and not accidentally use
        # the field's default value just because they aren't passed to __init__

        Item.objects.create(name="first", value=42)
        obj = Item.objects.only("name", "other_value").get(name="first")
        # Accessing "name" doesn't trigger a new database query. Accessing
        # "value" or "text" should.
        with self.assertNumQueries(0):
            self.assertEqual(obj.name, "first")
            self.assertEqual(obj.other_value, 0)

        with self.assertNumQueries(1):
            self.assertEqual(obj.value, 42)

        with self.assertNumQueries(1):
            self.assertEqual(obj.text, "xyzzy")

        with self.assertNumQueries(0):
            self.assertEqual(obj.text, "xyzzy")

        # Regression test for #10695. Make sure different instances don't
        # inadvertently share data in the deferred descriptor objects.
        i = Item.objects.create(name="no I'm first", value=37)
        items = Item.objects.only("value").order_by("-value")
        self.assertEqual(items[0].name, "first")
        self.assertEqual(items[1].name, "no I'm first")

        RelatedItem.objects.create(item=i)
        r = RelatedItem.objects.defer("item").get()
        self.assertEqual(r.item_id, i.id)
        self.assertEqual(r.item, i)

        # Some further checks for select_related() and inherited model
        # behavior (regression for #10710).
        c1 = Child.objects.create(name="c1", value=42)
        c2 = Child.objects.create(name="c2", value=37)
        Leaf.objects.create(name="l1", child=c1, second_child=c2)

        obj = Leaf.objects.only("name", "child").select_related()[0]
        self.assertEqual(obj.child.name, "c1")

        self.assertQuerysetEqual(
            Leaf.objects.select_related().only("child__name", "second_child__name"), [
                "l1",
            ],
            attrgetter("name")
        )

        # Models instances with deferred fields should still return the same
        # content types as their non-deferred versions (bug #10738).
        ctype = ContentType.objects.get_for_model
        c1 = ctype(Item.objects.all()[0])
        c2 = ctype(Item.objects.defer("name")[0])
        c3 = ctype(Item.objects.only("name")[0])
        self.assertTrue(c1 is c2 is c3)

        # Regression for #10733 - only() can be used on a model with two
        # foreign keys.
        results = Leaf.objects.only("name", "child", "second_child").select_related()
        self.assertEqual(results[0].child.name, "c1")
        self.assertEqual(results[0].second_child.name, "c2")

        results = Leaf.objects.only("name", "child", "second_child", "child__name", "second_child__name").select_related()
        self.assertEqual(results[0].child.name, "c1")
        self.assertEqual(results[0].second_child.name, "c2")

        # Test for #12163 - Pickling error saving session with unsaved model
        # instances.
        SESSION_KEY = '2b1189a188b44ad18c35e1baac6ceead'

        item = Item()
        item._deferred = False
        s = SessionStore(SESSION_KEY)
        s.clear()
        s["item"] = item
        s.save()

        s = SessionStore(SESSION_KEY)
        s.modified = True
        s.save()

        i2 = s["item"]
        self.assertFalse(i2._deferred)

        # Regression for #11936 - loading.get_models should not return deferred
        # models by default.
        klasses = sorted(
            cache.get_models(cache.get_app("defer_regress")),
            key=lambda klass: klass.__name__
        )
        self.assertEqual(
            klasses, [
                Child,
                Feature,
                Item,
                ItemAndSimpleItem,
                Leaf,
                Proxy,
                RelatedItem,
                ResolveThis,
                SimpleItem,
            ]
        )

        klasses = sorted(
            map(
                attrgetter("__name__"),
                cache.get_models(
                    cache.get_app("defer_regress"), include_deferred=True
                ),
            )
        )
        # FIXME: This is dependent on the order in which tests are run --
        # this test case has to be the first, otherwise a LOT more classes
        # appear.
        self.assertEqual(
            klasses, [
                "Child",
                "Child_Deferred_value",
                "Feature",
                "Item",
                "ItemAndSimpleItem",
                "Item_Deferred_name",
                "Item_Deferred_name_other_value_text",
                "Item_Deferred_name_other_value_value",
                "Item_Deferred_other_value_text_value",
                "Item_Deferred_text_value",
                "Leaf",
                "Leaf_Deferred_child_id_second_child_id_value",
                "Leaf_Deferred_name_value",
                "Leaf_Deferred_second_child_id_value",
                "Leaf_Deferred_value",
                "Proxy",
                "RelatedItem",
                "RelatedItem_Deferred_",
                "RelatedItem_Deferred_item_id",
                "ResolveThis",
                "SimpleItem",
            ]
        )

        # Regression for #16409 - make sure defer() and only() work with annotate()
        self.assertIsInstance(list(SimpleItem.objects.annotate(Count('feature')).defer('name')), list)
        self.assertIsInstance(list(SimpleItem.objects.annotate(Count('feature')).only('name')), list)

    def test_only_and_defer_usage_on_proxy_models(self):
        # Regression for #15790 - only() broken for proxy models
        proxy = Proxy.objects.create(name="proxy", value=42)

        msg = 'QuerySet.only() return bogus results with proxy models'
        dp = Proxy.objects.only('other_value').get(pk=proxy.pk)
        self.assertEqual(dp.name, proxy.name, msg=msg)
        self.assertEqual(dp.value, proxy.value, msg=msg)

        # also test things with .defer()
        msg = 'QuerySet.defer() return bogus results with proxy models'
        dp = Proxy.objects.defer('name', 'text', 'value').get(pk=proxy.pk)
        self.assertEqual(dp.name, proxy.name, msg=msg)
        self.assertEqual(dp.value, proxy.value, msg=msg)

    def test_resolve_columns(self):
        rt = ResolveThis.objects.create(num=5.0, name='Foobar')
        qs = ResolveThis.objects.defer('num')
        self.assertEqual(1, qs.count())
        self.assertEqual('Foobar', qs[0].name)

    def test_defer_with_select_related(self):
        item1 = Item.objects.create(name="first", value=47)
        item2 = Item.objects.create(name="second", value=42)
        simple = SimpleItem.objects.create(name="simple", value="23")
        related = ItemAndSimpleItem.objects.create(item=item1, simple=simple)

        obj = ItemAndSimpleItem.objects.defer('item').select_related('simple').get()
        self.assertEqual(obj.item, item1)
        self.assertEqual(obj.item_id, item1.id)

        obj.item = item2
        obj.save()

        obj = ItemAndSimpleItem.objects.defer('item').select_related('simple').get()
        self.assertEqual(obj.item, item2)
        self.assertEqual(obj.item_id, item2.id)

    def test_deferred_class_factory(self):
        from djangocg.db.models.query_utils import deferred_class_factory
        new_class = deferred_class_factory(Item,
            ('this_is_some_very_long_attribute_name_so_modelname_truncation_is_triggered',))
        self.assertEqual(new_class.__name__,
            'Item_Deferred_this_is_some_very_long_attribute_nac34b1f495507dad6b02e2cb235c875e')
