-- View: public.product_info_m_view

-- DROP MATERIALIZED VIEW IF EXISTS public.product_info_m_view;

CREATE MATERIALIZED VIEW IF NOT EXISTS public.product_info_m_view
TABLESPACE pg_default
AS
 SELECT product.product_name,
    product.description,
    product_type.product_category
   FROM product
     JOIN product_type ON product.product_type_id = product_type.product_type_id
WITH DATA;

ALTER TABLE IF EXISTS public.product_info_m_view
    OWNER TO postgres;