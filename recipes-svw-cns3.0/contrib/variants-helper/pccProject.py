class PccProject:
    def __init__(self, projectNumber, label, containerPrefix, trainPrefix, deliverUpdateContainer):
        self.projectNumber = projectNumber
        self.label = label
        self.containerPrefix = containerPrefix
        self.trainPrefix = trainPrefix
        self.deliverUpdateContainer = deliverUpdateContainer

    '''
    @return A project map.
    Key=ProjectNumber (see https://wiki-automotive.server.technisat-digital/x/4wj-Gg)
    Value=A ProjectObject
    '''
    @staticmethod
    def InitProjectList():
        result = dict();

        # PPC MQB:
        result[1] = PccProject(
                        projectNumber=1,
                        label='PPC MQB',
                        containerPrefix='',
                        trainPrefix='MOI3',
                        deliverUpdateContainer=True)

        # PPC 37W:
        result[2] = PccProject(
                        projectNumber=2,
                        label='PCC 37W',
                        containerPrefix='37W-',
                        trainPrefix='MOI3',
                        deliverUpdateContainer=True)

        # CNS
        result[3] = PccProject(
                        projectNumber=3,
                        label='CNS',
                        containerPrefix='',
                        trainPrefix='CNS3',
                        deliverUpdateContainer=True)

        # LG MQB
        result[4] = PccProject(
                        projectNumber=4,
                        label='LG MQB',
                        containerPrefix='',
                        trainPrefix='',
                        deliverUpdateContainer=False)

        # LG 37W
        result[5] = PccProject(
                        projectNumber=5,
                        label='LG 37W',
                        containerPrefix='37W-',
                        trainPrefix='',
                        deliverUpdateContainer=False)

        # ICAS MEB
        result[6] = PccProject(
                        projectNumber=6,
                        label='ICAS MEB',
                        containerPrefix='MEB-',
                        trainPrefix='',
                        deliverUpdateContainer=False)

        # CNS 37W
        result[7] = PccProject(
                        projectNumber=7,
                        label='CNS-37W',
                        containerPrefix='',
                        trainPrefix='CNS3',
                        deliverUpdateContainer=True)

        return result

    @staticmethod
    def ExtractProjectNo(systemVariantNo):
        # see https://wiki-automotive.server.technisat-digital/x/4wj-Gg for
        # systemVariantNo generation
        project=int(str(systemVariantNo[:-5]))
        return project

    @staticmethod
    def FromSystemVariantNo(systemVariantNo):
        projectNo = PccProject.ExtractProjectNo(systemVariantNo)
        projects = PccProject.InitProjectList()
        return projects[projectNo]
