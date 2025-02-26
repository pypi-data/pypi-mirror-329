import Rhino
import System
from typing import Union
import ast
import wood_rui


class Element:
    """
    Converts RhinoObject and its userstrings to geometry attributes.

    Element represents a Rhino Group objects made from two geometries:
    a) A Brep of Mesh with user strings that contain information about features, axis, radii, volumes, thickness, and joints.
    b) A polyline with three points that represents the plane of the group.
    This class helps to convert user strings to a python class with attributes and methods to manipulate the group.
    """

    def __init__(self, geometry_plane):
        self.geometry_plane: tuple[
            Rhino.DocObjects.RhinoObject, Rhino.Geometry.Plane
        ] = geometry_plane  # no need to be implemented

    ######################################################################
    # Properties
    ######################################################################

    @property
    def shape(self):
        """Return the shape of the element."""
        return self.geometry_plane[0].Geometry

    @shape.setter
    def shape(self, value):
        """Set the shape of the element."""

        replacement = value

        if isinstance(value, Rhino.Geometry.Mesh):
            replacement = value.DuplicateMesh()
        elif isinstance(value, Rhino.Geometry.Brep):
            replacement = value.DuplicateBrep()

        replacement.Transform(self.transformation)
        Rhino.RhinoDoc.ActiveDoc.Objects.Replace(self.geometry_plane[0].Id, replacement)
        Rhino.RhinoDoc.ActiveDoc.Views.Redraw()

    def shape_in_place(self, value):
        """Set the shape of the element in world space."""
        Rhino.RhinoDoc.ActiveDoc.Objects.Replace(self.geometry_plane[0].Id, value)
        Rhino.RhinoDoc.ActiveDoc.Views.Redraw()

    @property
    def plane(self):
        polyline_curve = self.geometry_plane[1].Geometry
        if polyline_curve.PointCount == 3:  # Ensure it has exactly 3 points
            polyline = polyline_curve.ToPolyline()
            origin = polyline[1]
            x_axis = polyline[0] - polyline[1]
            y_axis = polyline[2] - polyline[1]  # Corrected y-axis calculation
            return Rhino.Geometry.Plane(origin, x_axis, y_axis)
        return Rhino.Geometry.Plane.Unset

    def plane_axes(self, scale=1):
        plane = self.plane
        line0 = Rhino.Geometry.Line(
            plane.Origin, plane.Origin + plane.XAxis * scale
        ).ToNurbsCurve()
        line1 = Rhino.Geometry.Line(
            plane.Origin, plane.Origin + plane.YAxis * scale
        ).ToNurbsCurve()
        line2 = Rhino.Geometry.Line(
            plane.Origin, plane.Origin + plane.ZAxis * scale
        ).ToNurbsCurve()
        return [line0, line1, line2]

    @property
    def transformation(self):
        return Rhino.Geometry.Transform.PlaneToPlane(
            Rhino.Geometry.Plane.WorldXY, self.plane
        )

    @property
    def transformation_inverse(self):
        return Rhino.Geometry.Transform.PlaneToPlane(
            self.plane, Rhino.Geometry.Plane.WorldXY
        )

    ######################################################################
    # User Strings Attributes
    ######################################################################

    @property
    def name(self):
        return self.geometry_plane[0].Attributes.GetUserString("name")

    @name.setter
    def name(self, value):
        obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(self.geometry_plane[0].Id)
        obj.Attributes.SetUserString("name", value)
        obj.CommitChanges()

    @property
    def index(self):
        return int(self.geometry_plane[0].Attributes.GetUserString("index"))

    @index.setter
    def index(self, value):
        obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(self.geometry_plane[0].Id)
        obj.Attributes.SetUserString("index", str(value))
        obj.CommitChanges()

    @property
    def pair_indices(self):
        try:
            return ast.literal_eval(self.geometry_plane[0].Attributes.GetUserString("pair_indices"))
        except:
            return []

    @pair_indices.setter
    def pair_indices(self, value):
        obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(self.geometry_plane[0].Id)
        obj.Attributes.SetUserString("pair_indices", str(value))
        obj.CommitChanges()

    @property
    def neighbours(self):
        try:
            value = self.geometry_plane[0].Attributes.GetUserString("neighbours")
            return ast.literal_eval(value)
        except:
            return []

    @neighbours.setter
    def neighbours(self, value):
        obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(self.geometry_plane[0].Id)
        obj.Attributes.SetUserString("neighbours", str(value))
        obj.CommitChanges()

    @property
    def pair_neighbours(self):
        try:
            value = self.geometry_plane[0].Attributes.GetUserString("pair_neighbours")
            return ast.literal_eval(value)
        except: 
            return []

    @pair_neighbours.setter
    def pair_neighbours(self, value):
        obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(self.geometry_plane[0].Id)
        obj.Attributes.SetUserString("pair_neighbours", str(value))
        obj.CommitChanges()

    @property
    def features_count(self):
        count = 0
        string_dictionary = self.geometry_plane[0].Attributes.GetUserStrings()
        for key in string_dictionary:
            if "feature" in key:
                count += 1
        return count

    @property
    def features(self):
        geometries = []
        string_dictionary = self.geometry_plane[0].Attributes.GetUserStrings()
        for key in string_dictionary:
            if "feature" in key:
                value = string_dictionary[
                    key
                ]  # GetValues returns a list of values for the key
                geometry = Rhino.Geometry.GeometryBase.FromJSON(value)
                geometry.Transform(self.transformation)
                geometries.append(geometry)
        return geometries

    @features.setter
    def features(self, value):
        self.clear_features()
        
        feature_count = self.features_count
        self._features = value
        attributes = self.geometry_plane[0].Attributes.Duplicate()
        for idx, geometry in enumerate(value):
            geometry.Transform(self.transformation_inverse)
            opts = Rhino.FileIO.SerializationOptions()
            opts.WriteUserData = True
            json = geometry.ToJSON(opts)
            obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(self.geometry_plane[0].Id)
            attributes.SetUserString(f"feature_{feature_count + idx}", json)
            
        Rhino.RhinoDoc.ActiveDoc.Objects.ModifyAttributes(
            self.geometry_plane[0], attributes, False
        )
        self.geometry_plane[0].CommitChanges()

    def clear_features(self):
        attributes = self.geometry_plane[0].Attributes.Duplicate()
        for key in attributes.GetUserStrings():
            if "feature" in key:
                attributes.DeleteUserString(key)
        Rhino.RhinoDoc.ActiveDoc.Objects.ModifyAttributes(
            self.geometry_plane[0], attributes, False
        )

        self.geometry_plane[0].CommitChanges()

    @property
    def pair_polyline(self):
        value = self.geometry_plane[0].Attributes.GetUserString("pair_polyline")
        try:
            list3 = ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return []

        # convert triple nested lists to polylines
        polylines_list = []
        for list2 in list3:
            polylines = []
            for list1 in list2:
                polyline = Rhino.Geometry.Polyline()
                for i in range(0, len(list1), 3):
                    polyline.Add(
                        Rhino.Geometry.Point3d(list1[i], list1[i + 1], list1[i + 2])
                    )
                polyline.Transform(self.transformation)
                polylines.append(polyline)
            polylines_list.append(polylines)

        return polylines_list

    @pair_polyline.setter
    def pair_polyline(self, value):

        # Write polylines to user strings
        polylines_coordinates = []
        for i in range(0, len(value), 2):
            polyline0 = Rhino.Geometry.Polyline(value[i])
            polyline0.Transform(self.transformation_inverse)

            polyline1 = Rhino.Geometry.Polyline(value[i + 1])
            polyline1.Transform(self.transformation_inverse)

            polyline_coordinates0 = []
            for j in range(polyline0.Count):
                polyline_coordinates0.extend(
                    [polyline0[j].X, polyline0[j].Y, polyline0[j].Z]
                )

            polyline_coordinates1 = []
            for j in range(polyline1.Count):
                polyline_coordinates1.extend(
                    [polyline1[j].X, polyline1[j].Y, polyline1[j].Z]
                )

            polylines_coordinates.append([polyline_coordinates0, polyline_coordinates1])

        str_volumes = str(polylines_coordinates)

        obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(self.geometry_plane[0].Id)
        obj.Attributes.SetUserString("pair_polyline", str_volumes)
        obj.CommitChanges()

    @property
    def pair_polyline_merged(self):
        value = self.geometry_plane[0].Attributes.GetUserString("pair_polyline_merged")
        raise NotImplementedError("pair_polyline_merged is not implemented.")

    @pair_polyline_merged.setter
    def pair_polyline_merged(self, value):
        raise NotImplementedError("pair_polyline_merged is not implemented.")

    @property
    def axes(self):
        value = self.geometry_plane[0].Attributes.GetUserString("axes")
        list = ast.literal_eval(value)
        polylines = []
        for l in list:
            polyline = Rhino.Geometry.Polyline()
            for i in range(0, len(l), 3):
                polyline.Add(Rhino.Geometry.Point3d(l[i], l[i + 1], l[i + 2]))
            polyline.Transform(self.transformation)
            polylines.append(polyline)
        return polylines

    @axes.setter
    def axes(self, value):
        polylines_coordinates = []
        for polyline in value:
            polyline_transformed = polyline.Duplicate()
            polyline_transformed.Transform(self.transformation_inverse)
            coordinates = []
            for i in range(polyline_transformed.Count):
                coordinates.extend(
                    [
                        polyline_transformed[i].X,
                        polyline_transformed[i].Y,
                        polyline_transformed[i].Z,
                    ]
                )
            polylines_coordinates.append(coordinates)

        str_axes = str(polylines_coordinates)

        obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(self.geometry_plane[0].Id)
        obj.Attributes.SetUserString("axes", str_axes)
        obj.CommitChanges()

    @property
    def radii(self):
        value = self.geometry_plane[0].Attributes.GetUserString("radii")
        list = ast.literal_eval(value)
        return list

    @radii.setter
    def radii(self, value):
        obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(self.geometry_plane[0].Id)
        obj.Attributes.SetUserString("radii", str(value))
        obj.CommitChanges()

    @property
    def thickness(self):
        value = self.geometry_plane[0].Attributes.GetUserString("thickness")
        return float(value)

    @thickness.setter
    def thickness(self, value):
        obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(self.geometry_plane[0].Id)
        obj.Attributes.SetUserString("thickness", str(value))
        obj.CommitChanges()

    @property
    def insertion(self):
        value = self.geometry_plane[0].Attributes.GetUserString("insertion")

        if value == "-" or value is None:
            return [[] for _ in range(len(self.pair_polyline))]

        list_values = ast.literal_eval(value)
        lists_vectors = []
        for l in list_values:
            vectors = []
            for i in range(0, len(l), 3):
                vectors.append(Rhino.Geometry.Vector3d(l[i], l[i + 1], l[i + 2]))
            lists_vectors.append(vectors)
        return lists_vectors

    @insertion.setter
    def insertion(self, value):
        list_coordinates = []
        for list_vectors in value:
            coordinates = []
            for vector in list_vectors:
                coordinates.extend([vector.X, vector.Y, vector.Z])
            list_coordinates.append(coordinates)

        obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(self.geometry_plane[0].Id)
        obj.Attributes.SetUserString("insertion", str(coordinates))
        obj.CommitChanges()

    @property
    def joint_types(self):
        value = self.geometry_plane[0].Attributes.GetUserString("joint_types")

        if value == "-" or value is None:
            return [[] for _ in range(len(self.pair_polyline))]

        list_values = ast.literal_eval(value)
        return list_values

    @joint_types.setter
    def joint_types(self, value):
        obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(self.geometry_plane[0].Id)
        obj.Attributes.SetUserString("joint_types", str(value))
        obj.CommitChanges()

    ######################################################################
    # Methods
    ######################################################################

    def transform(self, transformation):
        """Orient element to target plane."""
        T = transformation
        geometry = self.geometry_plane[0].Geometry
        polyline = self.geometry_plane[1].Geometry
        geometry.Transform(T)
        polyline.Transform(T)
        Rhino.RhinoDoc.ActiveDoc.Objects.Replace(self.geometry_plane[0].Id, geometry)
        Rhino.RhinoDoc.ActiveDoc.Objects.Replace(self.geometry_plane[1].Id, polyline)
        Rhino.RhinoDoc.ActiveDoc.Views.Redraw()

    def transformed(self, transformation):
        """Orient element to target plane."""
        T = transformation
        guid0 = Rhino.RhinoDoc.ActiveDoc.Objects.Transform(
            self.geometry_plane[0], T, False
        )
        guid1 = Rhino.RhinoDoc.ActiveDoc.Objects.Transform(
            self.geometry_plane[1], T, False
        )
        obj_ref0 = Rhino.RhinoDoc.ActiveDoc.Objects.Find(guid0)
        obj_ref1 = Rhino.RhinoDoc.ActiveDoc.Objects.Find(guid1)

        obj_ref0.Attributes.RemoveFromAllGroups()
        obj_ref1.Attributes.RemoveFromAllGroups()
        obj_ref0.CommitChanges()
        obj_ref1.CommitChanges()

        group_index = Rhino.RhinoDoc.ActiveDoc.Groups.Add()
        Rhino.RhinoDoc.ActiveDoc.Groups.AddToGroup(group_index, guid0)
        Rhino.RhinoDoc.ActiveDoc.Groups.AddToGroup(group_index, guid1)
        obj_ref0.CommitChanges()
        obj_ref1.CommitChanges()

        Rhino.RhinoDoc.ActiveDoc.Views.Redraw()

    def _clean_brep(self, brep: Rhino.Geometry.Brep):
        copy = brep.DuplicateBrep()
        copy.Faces.SplitKinkyFaces()
        if Rhino.Geometry.BrepSolidOrientation.Inward == copy.SolidOrientation:
            copy.Flip()
        return copy

    def _clean_mesh(self, mesh: Rhino.Geometry.Mesh):
        copy = mesh.DuplicateMesh()
        copy.Compact()
        copy.Vertices.CombineIdentical(True, True)
        copy.Vertices.CullUnused()
        copy.UnifyNormals()
        copy.Weld(3.14159265358979)
        copy.FaceNormals.ComputeFaceNormals()
        copy.Normals.ComputeNormals()
        if copy.SolidOrientation() == -1:
            copy.Flip(True, True, True)
        return copy

    def _brep_boolean_difference(
        self, shape: Rhino.Geometry.Brep, cutters: list[Rhino.Geometry.Brep]
    ):
        shape_cleaned = self._clean_brep(shape)

        for brep in cutters:
            cutter_cleaned = self._clean_brep(brep)
            out_breps = Rhino.Geometry.Brep.CreateBooleanDifference(
                shape_cleaned,
                cutter_cleaned,
                Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance,
            )

            volume = 0

            if out_breps:
                for o in out_breps:
                    o_cleaned = self._clean_brep(o)
                    current_volume = Rhino.Geometry.VolumeMassProperties.Compute(
                        o_cleaned, True, False, False, False
                    ).Volume
                    if current_volume > volume:
                        volume = current_volume
                        shape_cleaned = o_cleaned

        return shape_cleaned

    def _mesh_boolean_difference(
        self, shape: Rhino.Geometry.Mesh, cutters: list[Rhino.Geometry.Mesh]
    ):
        shape_cleaned = self._clean_mesh(shape)

        for mesh in cutters:
            cutter_cleaned = self._clean_mesh(mesh)
            out_meshes = Rhino.Geometry.Mesh.CreateBooleanDifference(
                [shape_cleaned], [cutter_cleaned]
            )

            volume = 0

            if out_meshes:
                for o in out_meshes:
                    o_cleaned = self._clean_mesh(o)
                    current_volume = Rhino.Geometry.VolumeMassProperties.Compute(
                        o_cleaned, True, False, False, False
                    ).Volume
                    if current_volume > volume:
                        volume = current_volume
                        shape_cleaned = o_cleaned

        return shape_cleaned

    def boolean_difference(self):
        shape = self.shape
        features = self.features

        if isinstance(shape, Rhino.Geometry.Brep):
            result = self._brep_boolean_difference(shape, features)
            self.shape_in_place(result)
        elif isinstance(shape, Rhino.Geometry.Mesh):
            result = self._mesh_boolean_difference(shape, features)
            self.shape_in_place(result)

    ######################################################################
    # Static methods
    ######################################################################

    @staticmethod
    def get_first_axes(elements):
        return [element.axes[0] for element in elements]

    @staticmethod
    def get_first_radii(elements):
        return [element.radii[0] for element in elements]
        
    @staticmethod
    def loft_polylines_with_holes(input_curves0, input_curves1, color = System.Drawing.Color.Red):
        """
        Loft two sets of curves with holes.

        Parameters
        ----------
        input_curves0 : list[Rhino.Geometry.Curve]
            The curves of the first set.
        input_curves1 : list[Rhino.Geometry.Curve]
            The curves of the second set.
        color : System.Drawing.Color
            The color of the lofted solid.

        Returns
        -------
        Rhino.Geometry.Brep
            The lofted solid.
        
        """

        def project_curves_to_plane(curves):
            points = []
            for curve in curves:
                for point in curve.ToNurbsCurve().Points:
                    points.append(point.Location)

            result, plane = Rhino.Geometry.Plane.FitPlaneToPoints(points)

            xform = Rhino.Geometry.Transform.PlanarProjection(plane)
            curves_projected = []
            for curve in curves:
                curve_projected = curve.DuplicateCurve()
                curve_projected.Transform(xform)
                curves_projected.append(curve_projected)
            return curves_projected

        ###############################################################################
        # user input
        ###############################################################################

        if input_curves0 == [None]:
            return
        if input_curves1 == [None]:
            return

        if len(input_curves0) == 0:
            return
        if len(input_curves1) == 0:
            return

        flag = len(input_curves0) != 0 if True else len(input_curves1) != 0
        if flag:
            curves = []
            curves2 = []

            flag0 = len(input_curves1) == 0
            flag1 = len(input_curves0) == 0 and len(input_curves1) != 0
            flag2 = len(input_curves0) and len(input_curves1)

            if flag0:
                for i in range(len(input_curves0)):
                    if float(i) >= float(len(input_curves0)) * 0.5:
                        curves2.Add(input_curves0[i])
                    else:
                        curves.Add(input_curves0[i])
            elif flag1:
                for i in range(0, len(input_curves1), 2):
                    curves.Add(input_curves1[i])
                    curves2.Add(input_curves1[i + 1])
            elif flag2:
                curves = input_curves0
                curves2 = input_curves1

            input_curves0 = curves
            input_curves1 = curves2

        ###############################################################################
        # Create mesh of the bottom face
        ###############################################################################

        input_curves0 = project_curves_to_plane(input_curves0)
        brep_0 = Rhino.Geometry.Brep.CreatePlanarBreps(input_curves0, Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance)[0]

        input_curves1 = project_curves_to_plane(input_curves1)
        brep_1 = Rhino.Geometry.Brep.CreatePlanarBreps(input_curves1, Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance)[0]

        ###############################################################################
        # Create lofts
        ###############################################################################
        breps_to_join = [brep_0, brep_1]
        for i in range(len(input_curves0)):
            wall = Rhino.Geometry.Brep.CreateFromLoft(
                [input_curves0[i], input_curves1[i]],
                Rhino.Geometry.Point3d.Unset,
                Rhino.Geometry.Point3d.Unset,
                Rhino.Geometry.LoftType.Normal,
                False,
            )[0]
            breps_to_join.append(wall)

        ###############################################################################
        # Join Brep
        ###############################################################################

        solid = Rhino.Geometry.Brep.JoinBreps(breps_to_join, Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance)[0]

        faces = []
        for i in range(solid.Faces.Count):
            faces.append(solid.Faces[i].DuplicateFace(False))

        solid = Rhino.Geometry.Brep.JoinBreps(faces, Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance)[0]

        if solid:
            solid.Faces.SplitKinkyFaces(Rhino.RhinoMath.DefaultAngleTolerance, True)

            if Rhino.Geometry.BrepSolidOrientation.Inward is solid.SolidOrientation:
                solid.Flip()

        if color is not None:
            for i in range(solid.Faces.Count):
                solid.Faces[i].PerFaceColor = color
        else:
            for i in range(solid.Faces.Count):
                if i < 2:
                    solid.Faces[i].PerFaceColor = System.Drawing.Color.LightGray  # Color.LightGray
                else:
                    solid.Faces[i].PerFaceColor = System.Drawing.Color.DeepPink

        return solid
    
    @staticmethod
    def closest_axis(
        elements: list["Element"],
        distance: float,
        display_plane: bool,
        display_line: bool,
        intersection : bool,
    ) -> None:

        ###############################################################################
        # Extract axes and radii
        ###############################################################################
        curves : list[Rhino.Geometry.NurbsCurve] = []
        radii : list[float]= []
        for idx, element in enumerate(elements):
            curves.append(element.axes[0].ToNurbsCurve())
            radii.append(max(element.radii[0]))

        ###############################################################################
        # Run the closest point search
        ###############################################################################
        bboxes = []
        for idx, c in enumerate(curves):
            bbox: Rhino.Geometry.BoundingBox = c.GetBoundingBox(True)
            bbox.Inflate(radii[idx] + 0.02)
            bboxes.append(bbox)

        # create a tree
        rtree = Rhino.Geometry.RTree()

        # fill the tree
        for idx, bbox in enumerate(bboxes):
            rtree.Insert(bbox, idx)

        # call_backs of rtree
        def search_callback(sender, rtree_event_args):
            data_by_reference.append(rtree_event_args.Id)

        neighbours: list[list[int, int]] = []
        planes = []
        lines = []

        # Add Empty Layer and Delete everything from it.
        wood_rui.add_sub_layer(
            elements[0].geometry_plane[0],
            "nearest_axis",
            [],
            [System.Drawing.Color.Blue],
            True,
            True,
        )

        # perform search
        for i in range(len(bboxes)):
            data_by_reference = []
            if rtree.Search(bboxes[i], search_callback, data_by_reference):
                for j in data_by_reference:
                    if j <= i:
                        continue
                    result, p0, p1 = curves[i].ClosestPoints(curves[j])

                    if p0.DistanceTo(p1) < distance:
                        neighbours.append([i, j])

                        # Check if elements are parallel and they are lines
                        line0 = Rhino.Geometry.Line(
                            curves[i].PointAtStart, curves[i].PointAtEnd
                        )
                        line1 = Rhino.Geometry.Line(
                            curves[j].PointAtStart, curves[j].PointAtEnd
                        )
                        if (
                            abs(
                                line0.Direction.IsParallelTo(
                                    line1.Direction,
                                    Rhino.RhinoDoc.ActiveDoc.ModelAngleToleranceRadians,
                                )
                            )
                            == 1
                        ):
                            p0 = line0.PointAt(0.5)
                            p1 = line1.ClosestPoint(p0, True)

                        # Create plane from the closest lines and adjacent axes.
                        origin = (p0 + p1) * 0.5
                        z_axis = p1 - p0
                        if Rhino.Geometry.Vector3d.VectorAngle(
                            line1.Direction, -line0.Direction
                        ) > Rhino.Geometry.Vector3d.VectorAngle(
                            line0.Direction, -line1.Direction
                        ):
                            line1 = Rhino.Geometry.Line(
                                curves[j].PointAtEnd, curves[j].PointAtStart
                            )

                        y_axis = line0.Direction + line1.Direction
                        x_axis = Rhino.Geometry.Vector3d.CrossProduct(z_axis, y_axis)
                        plane = Rhino.Geometry.Plane(origin, x_axis, y_axis)

                        if (origin + plane.ZAxis).DistanceTo(p1) > (
                            origin - plane.ZAxis
                        ).DistanceTo(p1):
                            plane = Rhino.Geometry.Plane(origin, -x_axis, y_axis)

                        

                        # If boolean intersection is used plane can be recentered based on the shape
                        if intersection:
                            brep0 = elements[i].shape
                            brep1 = elements[j].shape
                            result = Rhino.Geometry.Brep.CreateBooleanIntersection(brep0, brep1, Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance)


                            if len(result) > 0:
                                
                                # no_oriented_brep = result[0].DuplicateBrep()
                                T = Rhino.Geometry.Transform.PlaneToPlane(plane, Rhino.Geometry.Plane.WorldXY)
                                result[0].Transform(T)
                                bbox = result[0].GetBoundingBox(True)

                                plane_from_intersection = Rhino.Geometry.Plane(
                                    bbox.Center,
                                    Rhino.Geometry.Vector3d.XAxis,
                                    Rhino.Geometry.Vector3d.YAxis
                                )
                                plane_from_intersection.Transform(Rhino.Geometry.Transform.PlaneToPlane(Rhino.Geometry.Plane.WorldXY, plane))
                                plane = plane_from_intersection

                                wood_rui.add_sub_layer(
                                    elements[i].geometry_plane[0],
                                    "nearest_axis_intersection",
                                    [result[0], bbox.ToBrep()],
                                    [System.Drawing.Color.Blue],
                                    i == 0,
                                    True,
                                )

                        planes.append(plane)

                        # Display Intersection Line
                        line = Rhino.Geometry.Line(p0, p1)
                        lines.append(line)
                        if display_plane:
                            line0 = Rhino.Geometry.Line(
                                plane.Origin, plane.XAxis * 100
                            ).ToNurbsCurve()
                            line1 = Rhino.Geometry.Line(
                                plane.Origin, plane.YAxis * 100
                            ).ToNurbsCurve()
                            line2 = Rhino.Geometry.Line(
                                plane.Origin, plane.ZAxis * 100
                            ).ToNurbsCurve()
                            plane_axes = [line0, line1, line2]
                            wood_rui.add_sub_layer(
                                elements[i].geometry_plane[0],
                                "nearest_axis",
                                plane_axes,
                                [System.Drawing.Color.Red, System.Drawing.Color.Green, System.Drawing.Color.Blue],
                                i == 0,
                                True,
                            )

                        if display_line:
                            wood_rui.add_sub_layer(
                                elements[i].geometry_plane[0],
                                "nearest_axis",
                                [line.ToNurbsCurve()],
                                [System.Drawing.Color.Blue],
                                i == 0,
                                True,
                            )

        ###############################################################################
        # Output
        ###############################################################################
        return neighbours, planes, lines



    ######################################################################
    # Create and Element with User Strings Attributes
    ######################################################################

    @staticmethod
    def add_element(
        shape: Union[Rhino.Geometry.Brep, Rhino.Geometry.Mesh],
        layer_name: str = "default",
        name: str = "beam",
        index: int = -1,
        neighbours: list[int] = [],
        features: list[Union[Rhino.Geometry.Brep, Rhino.Geometry.Mesh]] = [],
        pair_polyline: list[Rhino.Geometry.Polyline] = [],
        pair_polyline_merged: list[Rhino.Geometry.Polyline] = [],
        axes: list[Rhino.Geometry.Polyline] = [],
        radii: list[list[float]] = [],
        thickness: float = 0.0,
        insertion: list[list[Rhino.Geometry.Line]] = [],
        joint_types: list[Rhino.Geometry.TextDot] = [],
    ) -> None:
        """Add element with all its attributes for the wood joinery solver.

        Parameters
        ----------
        shape : Union[Rhino.Geometry.Brep, Rhino.Geometry.Mesh]
            The shape of the element. Final geometry is represented by one solid object.
        layer_name : str
            The name of the layer to add the geometry to.
        name : str
            The name of the element e.g. beam or plate.
        index : int
            The index of the element. Index is important when element are selected randomly.
        neighbours : list[int]
            The indices of the neighbouring elements.
        features : list[Union[Rhino.Geometry.Brep, Rhino.Geometry.Mesh]]
            The features of the element. Features are represented by multiple solid objects.
        pair_polyline : list[Rhino.Geometry.Polyline]
            The pair of polylines that represent the top and bottom of the element.
        pair_polyline_merged : list[Rhino.Geometry.Polyline]
            The pair of polylines that represent the top and bottom with joinery, specific to plates.
        axes : list[Rhino.Geometry.Polyline]
            The axes of the element.
        radii : list[list[float]]
            The radii of the axes.
        thickness : float
            The thickness of the element.
        insertion : list[Line]
            The insertion vectors of the element.
        joint_types : list[TextDot]
            The joints found by searching through the text dots.

        """

        print("Hi")

        ######################################################################
        # Add shape to Rhino document add assign plane on WorldXY.
        #   Create a layer: compas_wood::layer_name::element.
        #   Add geometry to the Rhino Canvas.
        #   Add a polyline to the Rhino Canvas to represnt a plane.
        ######################################################################

        # Create layer or find the existing one.
        layer_index = wood_rui.ensure_layer_exists(
            "compas_wood",
            layer_name,
            "shape",
            System.Drawing.Color.FromArgb(255, 30, 144, 255),
        )

        # Add the geometry to the Rhino document.
        if not shape:
            Rhino.RhinoApp.WriteLine("Attention: no shape to add.")
            return

        obj_guid = None

        if isinstance(shape, Rhino.Geometry.Mesh):
            obj_guid = Rhino.RhinoDoc.ActiveDoc.Objects.AddMesh(shape)
        elif isinstance(shape, Rhino.Geometry.Brep):
            obj_guid = Rhino.RhinoDoc.ActiveDoc.Objects.AddBrep(shape)
        else:
            Rhino.RhinoApp.WriteLine(
                "Attention: shape is not a mesh or brep: {}".format(type(shape))
            )
            return

        if not obj_guid:
            Rhino.RhinoApp.WriteLine("Attention: failed to add shape.")
            return

        obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(obj_guid)

        if not obj:
            Rhino.RhinoApp.WriteLine("Attention: failed to find shape.")
            return

        obj.Attributes.LayerIndex = layer_index

        # Plane, object frame and group polyline object.

        attributes = obj.Attributes.Duplicate()
        attributes.SetObjectFrame(Rhino.Geometry.Plane.WorldXY)
        Rhino.RhinoDoc.ActiveDoc.Objects.ModifyAttributes(obj, attributes, False)
        obj.CommitChanges()

        p0 = Rhino.Geometry.Point3d(0, 0, 0)
        p1 = p0 + Rhino.Geometry.Vector3d.XAxis * 0.1
        p2 = p0 + Rhino.Geometry.Vector3d.YAxis * 0.1
        groupframe = Rhino.Geometry.Polyline([p1, p0, p2])

        groupframe_guid = Rhino.RhinoDoc.ActiveDoc.Objects.AddPolyline(groupframe)
        if not groupframe_guid:
            print("Attention: failed to add group frame.")
            return
        groupframe_obj = Rhino.RhinoDoc.ActiveDoc.Objects.Find(groupframe_guid)
        if not groupframe_obj:
            print("Attention: failed to find group frame.")
            return

        group_index = Rhino.RhinoDoc.ActiveDoc.Groups.Add()
        Rhino.RhinoDoc.ActiveDoc.Groups.AddToGroup(group_index, obj_guid)
        Rhino.RhinoDoc.ActiveDoc.Groups.AddToGroup(group_index, groupframe_guid)

        ######################################################################
        # Go through individual attributes and assign the user strings.
        #   name : str = "beam",
        #   index : int = -1,
        #   neighbours : list[int] = [],
        #   features : list[Union[Rhino.Geometry.Brep, Rhino.Geometry.Mesh]] = [],
        #   pair_polyline : list[Rhino.Geometry.Polyline] = [],
        #   pair_polyline_merged : list[Rhino.Geometry.Polyline] = [],
        #   axes : list[Rhino.Geometry.Polyline] = [],
        #   radii : list[list[float]] = [],
        #   thickness : float = 0.0,
        #   insertion : list[Line] = [],
        #   joint_types : list[Rhino.Geometry.TextDot] = [],
        #   joint_volumes : list[list[Rhino.Geometry.Polyline]] = [],
        #   joint_lines : list[Rhino.Geometry.Polyline] = [],
        #   joint_areas : list[Rhino.Geometry.Polyline] = [],
        ######################################################################

        # name
        obj.Attributes.SetUserString("name", name if name else "-")

        # index
        obj.Attributes.SetUserString("index", str(index) if index else "-")

        # neighbours
        obj.Attributes.SetUserString(
            "neighbours", str(neighbours) if neighbours else "-"
        )

        # pair-index
        obj.Attributes.SetUserString("pair_indices", "-")

        # pair-neighbors
        obj.Attributes.SetUserString("pair_neighbours", "-")

        # features - this attribute can be missing when nothing is assigned
        for idx, feature in enumerate(features):
            if isinstance(feature, Rhino.Geometry.Mesh):
                opts = Rhino.FileIO.SerializationOptions()
                opts.WriteUserData = True
                json = feature.ToJSON(opts)
                obj.Attributes.SetUserString(f"feature_{idx}", json)
            elif isinstance(feature, Rhino.Geometry.Brep):
                opts = Rhino.FileIO.SerializationOptions()
                opts.WriteUserData = True
                opts.WriteAnalysisMeshes = False
                opts.WriteRenderMeshes = False
                json = feature.ToJSON(opts)
                obj.Attributes.SetUserString(f"feature_{idx}", json)

        # pair_polyline
        list_coordinates = []
        for idx, polyline in enumerate(pair_polyline):
            coordinates = []
            for i in range(polyline.Count):
                coordinates.extend([polyline[i].X, polyline[i].Y, polyline[i].Z])
            list_coordinates.append(coordinates)

        obj.Attributes.SetUserString(
            "pair_polyline", str(list_coordinates) if len(list_coordinates) > 0 else "-"
        )

        # pair_polyline_merged
        list_coordinates = []
        for idx, polyline in enumerate(pair_polyline_merged):
            coordinates = []
            for i in range(polyline.Count):
                coordinates.extend([polyline[i].X, polyline[i].Y, polyline[i].Z])
            list_coordinates.append(coordinates)

        obj.Attributes.SetUserString(
            "pair_polyline_merged",
            str(list_coordinates) if len(list_coordinates) > 0 else "-",
        )

        # axes
        bbox = shape.GetBoundingBox(True)
        str_axes = ""
        if not axes:
            str_axes = "[[0,0,0,0,0," + str(bbox.Max.Z - bbox.Min.Z) + "]]"
            axes = [
                Rhino.Geometry.Polyline(
                    [
                        Rhino.Geometry.Point3d(0, 0, 0),
                        Rhino.Geometry.Point3d(0, 0, bbox.Max.Z - bbox.Min.Z),
                    ]
                )
            ]
        else:
            axes = []
            for axis in axes:
                numbers = []
                for p in axes:
                    numbers.append(p.X)
                    numbers.append(p.Y)
                    numbers.append(p.Z)
            str_axes = str(axes)

        obj.Attributes.SetUserString("axes", str_axes)

        # radii - per polyline segment
        str_radii = ""
        if len(radii) == 0:
            distance = abs(bbox.Max.X - bbox.Min.X) * 0.5
            str_radii = "[[" + str(distance) + "]]"
        else:
            radii_matched_to_axes = []
            count = 0
            for axis in axes:
                numbers = []
                for j in range(len(axis) - 1):
                    numbers.append(radii[count % len(radii)])
                    count = count + 1
                radii_matched_to_axes.append(numbers)
            str_radii = str(radii_matched_to_axes)
        obj.Attributes.SetUserString("radii", str_radii)

        # thickness
        obj.Attributes.SetUserString("thickness", str(thickness) if thickness else "-")

        # insertion - this attribute must be handled by a seprate command using closest point search
        obj.Attributes.SetUserString("insertion", "-")
        for line in insertion:
            NotImplementedError(
                "Insertion is not implemented, closest point search is needed."
            )

        # joints_types - this attribute must be handled by a seprate command using closest point search
        obj.Attributes.SetUserString("joint_types", "-")
        for textdot in joint_types:
            NotImplementedError(
                "Joint types are not implemented, closest point search is needed."
            )

        # Commit changes and redraw
        obj.CommitChanges()
        Rhino.RhinoDoc.ActiveDoc.Views.Redraw()

        print("Hi")
    
        return obj, groupframe_obj

    def __repr__(self):
        return f"Element"
