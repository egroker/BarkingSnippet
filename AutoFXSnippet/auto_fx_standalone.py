# -------------- AUTO CACHE -----------------
@attr.s
class CacheAutoFx(Bead):
    precedent = HoudiniPrecedent
    houdini_api = attr.ib(type=HoudiniApi)  # type: HoudiniApi

    houdini_fx_scene_service = attr.ib(
        type=HoudiniFxSceneService
    )  # type: HoudiniFxSceneService

    logger = attr.ib(type=Logger)  # type: Logger

    def do(self, context):

        path = burton.get_platform_path(context.registered_file)
        houdini_file = self.houdini_api.load(path)

        nodes = self.houdini_api.get_all_sop_nodes_by_type(
            self.houdini_fx_scene_service.PUBLISH_NODE_TYPE
        )

        autoFx_nodes = [] 
        node_name = "auto_sim_"

        while nodes:
            node = nodes.pop(0)
            for input in node.inputs():
                if input == None:
                    continue
                elif node_name in input.name():
                    if input not in autoFx_nodes:
                        autoFx_nodes.append(input)
                else:
                    if input not in nodes:
                        nodes.append(input)

        for autoFx_node in autoFx_nodes:
            if autoFx_node:
                if autoFx_node.parm("hosts_mask"):
                    autoFx_node.parm("hosts_mask").set(self.precedent.hosts_mask)
                autoFx_node.parm("farm_sim").pressButton()
                self.logger.info(
                    "Started auto sim node: {}".format(autoFx_node.name())
                )
            else:
                self.logger.error(
                    "Can not find asset for auto farm simulation."
                )
                return BeadResponse(returned_signal=Bead.FAIL, context=context)

        return BeadResponse(returned_signal=Bead.OK, context=context)

@attr.s
class DispatchAutoFx(Bead):
    precedent = HoudiniPrecedent
    houdini_api = attr.ib(type=HoudiniApi)  # type: HoudiniApi

    afanasy_host_mask_resolver = attr.ib(
        type=AfanasyHostMaskResolver
    )  # type: AfanasyHostMaskResolver

    render_farm_service = attr.ib(
        type=RenderFarmService
    )  # type: RenderFarmService

    logger = attr.ib(type=Logger)  # type: Logger

    def do(self, context):
        from .utils import get_all_not_done_jobs

        hosts_mask = self.afanasy_host_mask_resolver.resolve_by_workplace(
            RenderFarmPool.LOCAL
        )

        path = burton.get_platform_path(context.registered_file)
        houdini_file = self.houdini_api.load(path)

        hip_name = "{}_{}_{}".format(context.entity, context.step, context.task)
        self.logger.info("Pattern fro search dependens: {}".format(hip_name))
        
        all_not_done_jobs_from_afwatch = get_all_not_done_jobs()
        job_names = []
        for not_done_job in all_not_done_jobs_from_afwatch:
            if(hip_name in not_done_job):
                job_names.append(not_done_job)

        related_job_depend_mask = ""
        if job_names:
            related_job_depend_mask = "|".join(job_names)
        else:
            self.logger.error("No jobs for dependencies found. Job started without them.")
        
        actions_first = []
        remote_chain_dispatch = RemoteChainAction(
            name="fx-DispatchFX",
            bead=DispatchFx,
            params={"hosts_mask": hosts_mask},
        )
        actions_first.append(remote_chain_dispatch)

        remote_create_preview = RemoteChainAction(
            name="fx-CreatePreviewAutoFx",
            bead=CreatePreviewAutoFx,
            depends_on=[remote_chain_dispatch],
            params={"hosts_mask": hosts_mask},
        )
        actions_first.append(remote_create_preview)

        remote_chain_config = RemoteChainConfig(
            label="Dispatch Auto FX and Create Preview",
            display_name="Dispatch Auto FX and Create Preview",
            actions=actions_first,
        )

        job_dispatch_fx = self.render_farm_service.send_remote_chain(
            remote_chain=remote_chain_config,
            context=context,
            job_depend_mask=related_job_depend_mask,
        )
        self.logger.info(
            "Running remote chain {}".format(job_dispatch_fx.name)
        )
        
        return BeadResponse(returned_signal=Bead.OK, context=context)
    
